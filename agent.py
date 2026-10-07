"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import mcp_client
import trace
from tools import suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "search_attempts": 0,        # includes one optional retry without size
        "dropped_constraints": {},  # original values removed for a retry
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    The query is parsed with regular expressions, then the loop advances
    through search, outfit suggestion, and fit-card creation. Each tool result
    is written to the session before the next step reads it back. An empty
    search result returns early, leaving the later session fields as None.

    Each logical tool boundary records its inputs and result through trace.py.
    ModelUnavailable is handled separately from programming errors so a model
    access problem ends with useful next steps instead of an exception label.
    """
    session = new_session(query, wardrobe)

    price_pattern = r"\bunder\s+\$?\s*(\d+(?:\.\d{1,2})?)\b"
    size_pattern = (
        r"\b(?:in\s+)?size\s+"
        r"((?:US\s+)?\d+(?:\.\d+)?|[A-Z]+\d*(?:/[A-Z]+\d*)?)\b"
    )

    price_match = re.search(price_pattern, query, flags=re.IGNORECASE)
    max_price = float(price_match.group(1)) if price_match else None
    without_price = re.sub(price_pattern, "", query, flags=re.IGNORECASE)

    size_match = re.search(size_pattern, without_price, flags=re.IGNORECASE)
    size = size_match.group(1) if size_match else None
    description = re.sub(size_pattern, "", without_price, flags=re.IGNORECASE)
    description = re.sub(r"\s+", " ", description).strip(" ,")

    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    next_step = "search_listings"
    iteration = 0

    while next_step:
        iteration += 1
        trace.check_iterations(iteration)

        if next_step == "search_listings":
            session["search_attempts"] += 1
            search_inputs = {
                "description": session["parsed"]["description"],
                "size": (
                    None
                    if "size" in session["dropped_constraints"]
                    else session["parsed"]["size"]
                ),
                "max_price": session["parsed"]["max_price"],
            }
            session["search_results"] = mcp_client.call_tool(
                "search_listings",
                search_inputs,
            )
            can_retry_without_size = (
                not session["search_results"]
                and session["parsed"]["size"] is not None
                and "size" not in session["dropped_constraints"]
            )
            trace.step(
                "search_listings (via MCP)",
                inputs=(
                    f"description={search_inputs['description']!r}, "
                    f"size={search_inputs['size']!r}, "
                    f"max_price={search_inputs['max_price']!r}"
                ),
                returned=session["search_results"],
                note=(
                    "branch: results found, continuing"
                    if session["search_results"]
                    else (
                        "branch: empty, retrying once without the size filter "
                        f"(dropped size={session['parsed']['size']!r})"
                        if can_retry_without_size
                        else "branch: empty, stopping"
                    )
                ),
            )

            if not session["search_results"]:
                if can_retry_without_size:
                    session["dropped_constraints"]["size"] = session["parsed"]["size"]
                    next_step = "search_listings"
                    continue

                changes = ["using different description words"]
                if (
                    session["parsed"]["size"] is not None
                    and "size" not in session["dropped_constraints"]
                ):
                    changes.append("changing or removing the size")
                if session["parsed"]["max_price"] is not None:
                    changes.append("raising the maximum price")
                retry_context = ""
                if "size" in session["dropped_constraints"]:
                    retry_context = (
                        " even after retrying without the size filter "
                        f"{session['dropped_constraints']['size']!r}"
                    )
                session["error"] = (
                    f"No listings matched{retry_context}. Try "
                    + " or ".join(changes)
                    + "."
                )
                return session

            session["selected_item"] = session["search_results"][0]
            next_step = "suggest_outfit"

        elif next_step == "suggest_outfit":
            outfit_inputs = (
                f"new_item={session['selected_item']['title']!r} "
                f"(id={session['selected_item']['id']}), "
                f"wardrobe_items={len(session['wardrobe'].get('items', []))}"
            )
            try:
                session["outfit_suggestion"] = suggest_outfit(
                    session["selected_item"],
                    session["wardrobe"],
                )
            except ModelUnavailable:
                session["error"] = (
                    "The styling model could not be reached, so I couldn't "
                    "finish this request. Try again later, or check the "
                    "configured model credentials."
                )
                trace.step(
                    "suggest_outfit",
                    inputs=outfit_inputs,
                    returned=session["error"],
                    note="model unavailable, stopping",
                )
                return session
            trace.step(
                "suggest_outfit",
                inputs=outfit_inputs,
                returned=session["outfit_suggestion"],
            )
            next_step = "create_fit_card"

        elif next_step == "create_fit_card":
            fit_card_inputs = (
                f"new_item={session['selected_item']['title']!r}; "
                f"outfit={session['outfit_suggestion']!r}"
            )
            try:
                session["fit_card"] = create_fit_card(
                    session["outfit_suggestion"],
                    session["selected_item"],
                )
            except ModelUnavailable:
                session["error"] = (
                    "The styling model could not be reached, so I couldn't "
                    "finish this request. Try again later, or check the "
                    "configured model credentials."
                )
                trace.step(
                    "create_fit_card",
                    inputs=fit_card_inputs,
                    returned=session["error"],
                    note="model unavailable, stopping",
                )
                return session
            trace.step(
                "create_fit_card",
                inputs=fit_card_inputs,
                returned=session["fit_card"],
            )
            next_step = None

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
