# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr lets a user describe a secondhand clothing item they want, optionally
including a size and maximum price. It searches the available starter listings
and selects the first result from the ranked matches. Using that listing and
the user's wardrobe information, it suggests one or two outfits; if the
wardrobe is empty, it gives general styling advice instead. Finally, it creates
a short fit-card caption based on the selected listing and outfit suggestion.

---

## Tool Inventory

### `search_listings(description, size, max_price)`

- **What it does:** Loads the starter listing data, applies the optional size
  and inclusive maximum-price filters, scores the remaining listings by
  case-insensitive keyword overlap with the requested description, and puts
  the best matches first. Size matching uses whole size tokens: for example,
  `M` matches `S/M`, but `L` does not match `XL` and `S` does not match `US 9`.
- **Inputs:** `description` (`str`) — required search words; `size`
  (`str | None`, default `None`) — an optional size filter; `max_price`
  (`float | None`, default `None`) — an optional inclusive price ceiling.
- **Returns:** `list[dict]` containing up to `config.SEARCH_RESULT_LIMIT` full
  listing dictionaries, ordered from highest to lowest keyword-overlap score.
  Each dictionary retains the starter fields `id`, `title`, `description`,
  `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`,
  and `platform`.
- **When it has nothing:** If no listing passes the filters and shares a
  description keyword, returns `[]`, not `None`.

### `suggest_outfit(new_item, wardrobe)`

- **What it does:** Uses the starter model adapter to suggest one or two ways
  to style the selected listing, naming compatible pieces from the user's
  wardrobe when those pieces are available.
- **Inputs:** `new_item` (`dict`) — the selected full listing dictionary;
  `wardrobe` (`dict`) — a dictionary whose `items` key contains a
  `list[dict]` of wardrobe items.
- **Returns:** A non-empty `str` containing one or two outfit suggestions.
- **When it has nothing:** When `wardrobe["items"]` is empty, returns a
  non-empty string with useful general styling advice for `new_item` instead
  of raising an exception or returning an empty string.

### `create_fit_card(outfit, new_item)`

- **What it does:** Uses the starter model adapter to turn an outfit suggestion
  and its selected listing into a short caption someone could realistically
  post.
- **Inputs:** `outfit` (`str`) — the result from `suggest_outfit`; `new_item`
  (`dict`) — the selected full listing dictionary.
- **Returns:** A `str` containing a two-to-four-sentence caption that mentions
  the item, its price, and its platform once each and describes a specific
  vibe.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a
  non-empty descriptive message explaining that no outfit suggestion was
  available, rather than raising an exception or returning an empty string.

---

## Planning Loop

**Branch rule:** If `search_listings` returns `[]`, put a useful message in
`session["error"]` that names something the user can change in the search, and
stop immediately before either model-backed tool is called. Otherwise, store
the results, select the first listing, store it in `session["selected_item"]`,
and continue through `suggest_outfit` and `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**MCP routing:** The search step calls
`mcp_client.call_tool("search_listings", arguments)`. The registered tool in
`mcp_server.py` delegates to the existing `tools.py::search_listings`
implementation, and `mcp_client.py` unwraps the response back into the same
`list[dict]` shape before it enters session state.

**How the query is parsed:** Deterministic string parsing in
`agent.py::run_agent`: extract an `under $...` price and an explicit size when
present, then use the remaining item words as the description.

**What moves through the session:** `parsed` → `search_results` →
`selected_item` → `outfit_suggestion` → `fit_card`. Each tool reads the value
stored by the previous step back from the session before it is called; the
selected item is also read from the session again for `create_fit_card`.

---

## Sample Run

**One full query**

```text
PS> python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Y2K Streetwear**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The fitted, cropped silhouette of the baby tee balances the volume of the high-waisted baggy jeans, hitting the exact Y2K proportion. Layering the slightly cropped black denim jacket keeps the waistline defined, while the chunky sneakers tie the retro streetwear aesthetic together.

***

**Outfit 2: Casual Contrast**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt, Black crossbody bag, Black combat boots

**Why it works:** Pairing the ultra-feminine, pink-and-purple butterfly tee with utilitarian khaki trousers creates an intentional high-low mix. Tucking the tee in and adding the brown leather belt pulls the earth tones of the trousers together with the warm tones in the graphic.

  Fit card: Channeling peak 2000s energy with this butterfly print Y2K baby tee, listed on Depop for just $18. I love wearing it tucked into wide-leg khaki trousers with chunky combat boots for that effortless high-low contrast. It gives total vintage mall-rat chic.

2 model calls this session, 871 prompt + 308 output tokens
```

**The three tools, tested one at a time**

```text
PS> python -c "from tools import search_listings; print([(item['title'], item['size'], item['price']) for item in search_listings('graphic tee', size='L', max_price=30)])"
[('Graphic Tee — 2003 Tour Bootleg Style', 'L', 24.0), ('Vintage Band Tee — Faded Grey', 'L', 19.0), ('Vintage Graphic Hoodie — Faded Black', 'L', 26.0)]
```

```text
PS> python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1: Casual Streetwear**
*   **Tops:** White ribbed tank top
*   **Bottoms:** Vintage Levi's 501 Jeans (Medium wash)
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The white ribbed tank tucked into the medium wash 501s creates a clean, classic base. Adding the cropped black denim jacket introduces a cool black-and-blue contrast, while the chunky white sneakers and black crossbody tie the streetwear aesthetic together.

***

**Outfit 2: Relaxed Layers**
*   **Tops:** Oversized grey crewneck sweatshirt
*   **Bottoms:** Vintage Levi's 501 Jeans (Medium wash)
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** The grey crewneck's hip-length drop contrasts nicely with the straight-leg fit of the 501s. Tucking the hem slightly at the front allows the brown leather belt to peek through, grounding the look before finishing with rugged black combat boots.
```

```text
PS> python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('Pair it with a white ribbed tank and chunky white sneakers.', load_listings()[0]))"
Nothing beats the feel of truly broken-in denim, and these Vintage Levi's 501 Jeans deliver all the right vintage vibes. I'm styling this W30 L30 pair with a crisp white ribbed tank for an effortless, everyday look. Grab them on Depop for just $38.00 before I change my mind!
```

---

## How I Used AI

### AI use example 1 — Acceptance criteria

- **What I asked:** I asked Claude to inspect the starter criteria and explain
  what my three additional criteria needed to measure without writing them for
  me.
- **What the AI returned:** It identified three observable areas: whether the
  selected listing survives the session-state handoff, whether the fit card
  preserves useful item and styling details, and whether an empty wardrobe is
  handled without an error.
- **What I changed or decided:** I selected and supplied Criteria 3–5 around
  those areas, then adjusted the wording so each has a measurable target: 5 of
  5 for deterministic state transfer and empty-wardrobe handling, and at least
  4 of 5 for model-generated fit-card quality.

### AI use example 2 — Planning loop

- **What I asked:** I asked Claude to finish Milestone 5 using the starter's
  existing session dictionary, with a real empty-search branch and values read
  back from session before each later tool call.
- **What the AI returned:** Claude found that `run_agent()` was still the starter
  stub: it created a session, stored a "planning loop isn't built yet" error,
  and returned without calling any tool.
- **What I changed or decided:** I implemented deterministic regular-expression
  parsing for description, size, and maximum price, then added a three-step
  planning loop in `agent.py`. Search results, the selected listing, the outfit
  suggestion, and the final fit card now move through session state; an empty
  search stores actionable advice and returns before either model-backed tool
  runs.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | At least 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item stays the same across session state | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes the selected item and a styling detail | At least 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe returns general styling advice without an error | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

The complete unedited output for all 25 tries is in
`results/run_2026-10-06_1145_before.md`. The evidence below is copied from
Try 1 of each scenario.

### Criterion 1 evidence

Source: `agent.py` — `run_agent()`; captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:

Channeling major 2000s pop-star energy in this Y2K butterfly baby tee, scored on Depop for just $18. I love balancing the cropped fit by pairing it with baggy dark-wash jeans and chunky white sneakers. It's giving ultimate nostalgic streetwear vibes. ✨🦋

Trace:

[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear** *   **Top:** Y2K Butterfly Baby Tee *   **Bottoms:** Baggy straight-leg jeans (da…
[3] create_fit_card
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear**\n*   **Top:** Y2K Butterfly Ba…
      out: Channeling major 2000s pop-star energy in this Y2K butterfly baby tee, scored on Depop for just $18. I love ba…
```

### Criterion 2 evidence

Source: `agent.py` — `run_agent()`; captured by `run_eval.py` — `run_once()`

```text
- stopped early: yes — No listings matched. Try using different description words or changing or removing the size or raising the maximum price.
- selected_item: (none)
- search_results: 0

Trace:

[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping
```

### Criterion 3 evidence

Source: `agent.py` — `run_agent()`; captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 7

[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe' (id=lst_004), wardrobe_items=10
      out: **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy straight-leg jeans (…
```

### Criterion 4 evidence

Source: `tools.py` — `create_fit_card()` via `agent.py` — `run_agent()`;
captured by `run_eval.py` — `run_once()`

```text
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)

Outfit suggestion:

**Outfit 1: High-Contrast Denim (Double Denim)**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Light wash cropped denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

Fit card:

Found this dreamy light wash cropped denim jacket on Poshmark for just $42. I love the structured shoulders, so I’m styling it with baggy dark-wash jeans and a white tank for the ultimate effortless streetwear look. It's the ultimate blank canvas for my wardrobe.
```

### Criterion 5 evidence

Source: `tools.py` — `suggest_outfit()` via `agent.py` — `run_agent()`;
captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

Buy it. At $42, a cropped light-wash denim jacket with good structure is a versatile layering staple.

**Two ways to style it using common basics:**

1. **Casual Contrast:** Layer it over a plain white crewneck t-shirt paired with black straight-leg trousers and white leather sneakers. The light blue wash pops against dark pants, and the crop balances the relaxed trousers.
2. **Monochromatic Denim:** Pair it with black skinny jeans and a fitted black tank top, finished off with black ankle boots. The jacket serves as a bright, structured focal point over a sleek base.

[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=0
      out: Buy it. At $42, a cropped light-wash denim jacket with good structure is a versatile layering staple.   **Two …
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```text
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear** *   **Top:** Y2K Baby Tee — Butterfly Print *   **Bottoms:** Baggy straight-leg j…
[3] create_fit_card
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear**\n*   **Top:** Y2K Baby Tee — B…
      out: Channeling peak 2000s energy with this butterfly print Y2K baby tee, listed on Depop for just $18. I love wear…
```

**Empty search**

```text
[1] search_listings (via MCP)
      in:  description='diamond-encrusted astronaut tuxedo', size=None, max_price=2.0
      out: [] (empty)
      →    branch: empty, stopping
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

`agent.py::run_agent` calls `mcp_client.call_tool("search_listings", ...)`;
`mcp_server.py` registers that one tool and delegates to
`tools.py::search_listings`. The MCP client normalizes the response back to the
same `list[dict]` used by session state, so the logical search result and later
planning-loop behavior remained the same after the rewire.

### Failure-mode checks

These messages came from real command-line runs during Milestone 2.

**Empty search** — command:
`python app.py ask 'diamond-encrusted astronaut tuxedo under $2'`

```text
No listings matched. Try using different description words or raising the maximum price.
```

**Empty wardrobe** — command:
`python app.py ask 'vintage graphic tee under $30' --empty-wardrobe`

```text
Since your wardrobe is currently empty, here are two ways to style this baby tee using common, versatile basics:

1. **Casual Denim Look:** Pair the fitted baby tee with high-waisted, straight-leg or baggy light-wash jeans to balance the Y2K silhouette. Finish with white canvas sneakers and a simple shoulder bag.
2. **Skater/Edgy Contrast:** Layer it with a pleated black tennis skirt or cargo trousers. Add chunky platform sneakers or combat boots to give the sweet butterfly graphic a cool, contrasting edge.
```

**Model unavailable** — a new, uncached query was run with a deliberately
invalid process-local API credential; the real credential was neither printed
nor changed on disk. The query was
`saffron butterfly baby tee moonbeam under $19`.

```text
The styling model could not be reached, so I couldn't finish this request. Try again later, or check the configured model credentials.
```


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
