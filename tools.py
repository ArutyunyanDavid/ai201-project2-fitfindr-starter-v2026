"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def _tokens(value: str) -> set[str]:
    """Return lowercase word/number tokens for search and size matching."""
    return set(re.findall(r"[a-z]+|\d+(?:\.\d+)?", value.casefold()))


def _size_matches(requested: str, listed: str) -> bool:
    """Match whole size tokens so, for example, M matches S/M but not medium."""
    requested_tokens = _tokens(requested)
    return bool(requested_tokens) and requested_tokens <= _tokens(listed)

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    query_tokens = _tokens(description)
    scored: list[tuple[int, dict]] = []

    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if size and not _size_matches(size, listing["size"]):
            continue

        searchable_parts = [
            listing["title"],
            listing["description"],
            listing["category"],
            listing["condition"],
            listing["size"],
            listing["brand"] or "",
            listing["platform"],
            *listing["style_tags"],
            *listing["colors"],
        ]
        score = len(query_tokens & _tokens(" ".join(searchable_parts)))
        if score:
            scored.append((score, listing))

    scored.sort(key=lambda match: match[0], reverse=True)
    return [listing for _, listing in scored[:config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def _listing_details(item: dict) -> str:
    """Format the listing fields the model needs without changing the item."""
    return "\n".join([
        f"Title: {item.get('title', 'Unknown item')}",
        f"Description: {item.get('description', '')}",
        f"Category: {item.get('category', '')}",
        f"Size: {item.get('size', '')}",
        f"Price: ${item.get('price', 0):.2f}",
        f"Colors: {', '.join(item.get('colors', []))}",
        f"Style tags: {', '.join(item.get('style_tags', []))}",
        f"Platform: {item.get('platform', '')}",
    ])


def _wardrobe_item_details(item: dict) -> str:
    """Format one wardrobe item for the outfit prompt."""
    details = [
        item.get("name", "Unnamed item"),
        f"category: {item.get('category', '')}",
        f"colors: {', '.join(item.get('colors', []))}",
        f"style tags: {', '.join(item.get('style_tags', []))}",
    ]
    if item.get("notes"):
        details.append(f"notes: {item['notes']}")
    return "; ".join(details)

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    wardrobe_items = wardrobe.get("items", [])
    item_details = _listing_details(new_item)
    system = (
        "You are a practical personal stylist. Give concise, specific advice "
        "and do not claim the user owns anything not listed in their wardrobe."
    )

    if not wardrobe_items:
        prompt = (
            "The user is considering this thrifted item:\n"
            f"{item_details}\n\n"
            "Their wardrobe is empty, so give one or two useful general "
            "styling recommendations using common basics. Do not refer to "
            "specific pieces as items they already own."
        )
        fallback = (
            f"Try styling the {new_item.get('title', 'selected item')} with "
            "simple neutral basics, comfortable shoes, and one coordinating "
            "layer or accessory."
        )
    else:
        wardrobe_text = "\n".join(
            f"- {_wardrobe_item_details(item)}" for item in wardrobe_items
        )
        prompt = (
            "The user is considering this thrifted item:\n"
            f"{item_details}\n\n"
            "Their wardrobe contains:\n"
            f"{wardrobe_text}\n\n"
            "Suggest one or two complete outfits. Name the exact wardrobe "
            "pieces you use and explain briefly why each combination works."
        )
        fallback = (
            f"Pair the {new_item.get('title', 'selected item')} with a "
            "compatible piece from the wardrobe and finish with simple shoes "
            "and an accessory."
        )

    response = generate(prompt, system=system).strip()
    return response or fallback


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    outfit = outfit.strip()
    if not outfit:
        return "No fit card was created because no outfit suggestion was available."

    title = new_item.get("title", "selected item")
    price = new_item.get("price", 0)
    platform = new_item.get("platform", "the listing platform")
    prompt = (
        "Write a short social caption for this thrift find.\n\n"
        f"Selected listing:\n{_listing_details(new_item)}\n\n"
        f"Outfit suggestion:\n{outfit}\n\n"
        "Write two to four sentences. Use the selected listing title exactly "
        "as shown, mention its price and platform exactly once each, include "
        "at least two concrete styling details from the outfit suggestion, "
        "and describe a specific "
        "vibe. Make it sound like something a person would post, not a product "
        "description. Return only the caption."
    )
    system = "You write concise, natural social captions about thrifted outfits."
    fallback = (
        f"Found the {title} for ${price:.2f} on {platform}. "
        f"Style it like this: {outfit}"
    )
    response = generate(prompt, system=system).strip()
    return response or fallback
