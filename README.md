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

**MCP routing:** The search and fit-card steps call
`mcp_client.call_tool(...)`. The registered wrappers in `mcp_server.py`
delegate to `tools.py::search_listings` and `tools.py::create_fit_card`, while
`mcp_client.py` unwraps their responses back into the original `list[dict]`
and `str` shapes before they enter session state. `suggest_outfit` remains a
direct tool call.

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

### AI use example 3 — MCP, traces, and Before/After evaluation

- **What I asked:** I asked Codex to preserve the existing project while
  routing `search_listings` through MCP, triggering the three required failure
  modes, reading the traces, and comparing one targeted improvement with the
  same five evaluation scenarios.
- **What the AI returned:** Codex helped verify the MCP response boundary,
  identify a targeted model-unavailable handler, organize the trace and
  criterion evidence, and strictly count the Before and After results against
  the original targets.
- **What I changed or decided:** I kept the original criteria and scenarios,
  documented that every Before criterion was already MET, and made one
  prompt-only change to test whether exact-title and styling-detail fidelity
  improved without changing the scored targets.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Stretch Features — Declared Before Build

I am declaring these three stretch features before implementing them:

1. **Second tool on MCP (+1):** Move `create_fit_card` behind the MCP
   client/server boundary alongside `search_listings`, preserve its logical
   string return value, and record a trace showing both MCP tool calls.
2. **Retry with looser constraints (+1):** When an initial search with an
   explicit size returns `[]`, retry exactly once without the size filter. The
   trace will name the dropped size constraint, and a second empty result will
   still stop before the model-backed tools.
3. **Second measured improvement (+2):** Treat the size-filter retry as one
   isolated second improvement, then run the same five scenarios five times
   with caching off and add a third run log comparing it with the After run.

The retry will be implemented and measured before the second MCP move so the
third run can be attributed to one behavior change.

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

### Criterion 1 — A matching query completes all three tools

**Original criterion:** Given a query that matches at least one listing, the
agent completes all three tool calls and returns a fit card — in at least 4 of
5 tries.

**Target:** At least 4 of 5

**Results:** PASS, PASS, PASS, PASS, PASS

**Verdict:** MET (5/5)

**How decided:** All five traces contain `search_listings`, `suggest_outfit`,
and `create_fit_card`, and every try returned a fit card, so 5 passes meets the
target of at least 4.

### Criterion 2 — An impossible query stops before the second tool

**Original criterion:** Given a query that matches no listings, the agent stops
before calling `suggest_outfit` and returns a message naming what to change — 5
of 5 tries.

**Target:** 5 of 5

**Results:** PASS, PASS, PASS, PASS, PASS

**Verdict:** MET (5/5)

**How decided:** Each of the five tries stopped after the empty
`search_listings` result, omitted `suggest_outfit`, and suggested changing the
description, size, or maximum price, so all 5 required tries passed.

### Criterion 3 — The selected item stays the same across session state

**Original criterion:** Given a query that returns at least one listing, the
item stored in `session["selected_item"]` is the same listing passed into
`suggest_outfit` — in 5 of 5 tries.

**Target:** 5 of 5

**Results:** PASS, PASS, PASS, PASS, PASS

**Verdict:** MET (5/5)

**How decided:** In every try, session stored `90s Track Jacket — Navy/White
Stripe` and the `suggest_outfit` trace received that same title and listing ID
`lst_004`, so all 5 required tries passed.

### Criterion 4 — The fit card includes useful information about the selected item

**Original criterion:** Given a successful search and outfit suggestion, the
final fit card names the selected item and includes at least one styling detail
from the outfit suggestion — in at least 4 of 5 tries.

**Target:** At least 4 of 5

**Results:** PASS, PASS, PASS, PASS, PASS

**Verdict:** MET (5/5)

**How decided:** All five fit cards named the light-wash cropped denim jacket
and reused at least one concrete outfit detail, including jeans, a white tank,
a hoodie, sneakers, a sweatshirt, or khaki trousers, so 5 passes exceeds the
target of at least 4.

### Criterion 5 — An empty wardrobe does not cause the agent to fail

**Original criterion:** Given an empty wardrobe, `suggest_outfit` returns at
least one general styling recommendation and does not raise an error — in 5 of
5 tries.

**Target:** 5 of 5

**Results:** PASS, PASS, PASS, PASS, PASS

**Verdict:** MET (5/5)

**How decided:** Every trace passed `wardrobe_items=0` to `suggest_outfit`, and
all five responses returned multiple general styling recommendations without
an error, so all 5 required tries passed.

### Patterns Across Misses

There were no misses, so there is no shared failure pattern and no
Step/Mechanism diagnosis to report. No criterion was revised. In a future
evaluation, Criterion 4 could reasonably be made stricter because it passed 5
of 5: it could require every fit card to preserve the exact listing title and
two concrete styling details, rather than one, while leaving this original
criterion and result unchanged.

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

For the required Milestone 1 move, `agent.py::run_agent` called
`mcp_client.call_tool("search_listings", ...)`; `mcp_server.py` delegated to
`tools.py::search_listings`, and the client normalized the response back to the
same `list[dict]`. The earlier trace above records that pre-bonus architecture.
The separately declared second MCP tool is documented with its own post-build
trace below.

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

**What I changed:** I changed one instruction in
`tools.py::create_fit_card`. The prompt now asks the model to use the selected
listing title exactly as shown and include at least two concrete details from
the outfit suggestion. Previously, it asked the model to name the item and
include at least one outfit detail.

**Why I picked it:** Milestone 4 found no missed criterion and therefore no
failure diagnosis to fix. Its only documented improvement opportunity was a
stricter future version of Criterion 4: the Before cards passed the original
criterion, but they could paraphrase the listing title and satisfy it with only
one styling detail. This experiment proactively hardens that model-output step
without inventing a missed result.

**Expected effect:** Criterion 4 only. The intended effect was stronger title
and styling-detail fidelity; the original criterion, target, scenarios, loop,
session handling, tool return shapes, model settings, and cache-off evaluation
mode remained unchanged.

**Relevant file and function:** `tools.py::create_fit_card`

**MCP note:** `search_listings` still runs through
`agent.py` → `mcp_client.py` → `mcp_server.py` →
`tools.py::search_listings` rather than being called directly by the loop. Its
logical `list[dict]` result did not change after the MCP move; only the call
path changed.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | At least 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item stays the same across session state | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes the selected item and a styling detail | At least 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe returns general styling advice without an error | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

The complete unedited output for all 25 After tries is in
`results/run_2026-10-06_1214_after.md`. The evidence below is copied from Try
1 of each scenario.

#### Criterion 1 evidence — After

Source: `agent.py` — `run_agent()`; captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:

Channeling total 2000s streetwear energy with this Y2K Baby Tee — Butterfly Print. I love balancing the fitted crop with baggy straight-leg jeans and chunky white sneakers. Grab this vintage gem on Depop for just $18.00 before it’s gone!

Trace:

[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear** *   **Top:** Y2K baby tee *   **Bottoms:** Baggy straight-leg jeans (dark blue) *…
[3] create_fit_card
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear**\n*   **Top:** Y2K baby tee\n* …
      out: Channeling total 2000s streetwear energy with this Y2K Baby Tee — Butterfly Print. I love balancing the fitted…
```

#### Criterion 2 evidence — After

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

#### Criterion 3 evidence — After

Source: `agent.py` — `run_agent()`; captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 7

[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe' (id=lst_004), wardrobe_items=10
      out: **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy straight-leg jeans (…
```

#### Criterion 4 evidence — After

Source: `tools.py` — `create_fit_card()` via `agent.py` — `run_agent()`;
captured by `run_eval.py` — `run_once()`

```text
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)

Outfit suggestion:

**Outfit 1: High-Contrast Denim (Double Denim)**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Denim jacket (light wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

Fit card:

Double denim is having a serious moment, and this thrifted Denim Jacket — Light Wash, Cropped is the ultimate blank canvas for it. I love styling it with baggy dark wash jeans and chunky white sneakers for that effortless streetwear edge. Grab it on Poshmark for just $42.00 before I change my mind!
```

#### Criterion 5 evidence — After

Source: `tools.py` — `suggest_outfit()` via `agent.py` — `run_agent()`;
captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

**Verdict: Buy.** At $42, a cropped light-wash denim jacket is a versatile year-round staple.

**How to style it using common basics:**
1. **High-Rise Casual:** Pair it with a white cotton t-shirt, high-waisted black straight-leg trousers, and white leather sneakers. The high rise balances the cropped hem of the jacket.
2. **Contrast Textures:** Layer it over a black ribbed midi dress with canvas slip-on sneakers for an easy, balanced look between fitted and structured.

[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=0
      out: **Verdict: Buy.** At $42, a cropped light-wash denim jacket is a versatile year-round staple.  **How to style …
```

**Did it help, and how do I know:** The change made no measurable difference
to the original acceptance criteria: Before and After were both 5 of 5 on all
five criteria. The stronger, unscored prompt goal did appear in all five
Criterion 4 After cards—they used the exact listing title and at least two
outfit details—but that does not change the original criterion's score.



---

## What's Still Broken

No tested criterion remains MISSED after the improvement: Criteria 1–5 are all
MET at 5 of 5 against their original targets, so there is no remaining miss to
diagnose or list as broken.

A known limitation remains outside those passing scores: the outfit and
fit-card steps depend on an external model, so a service or credential failure
can prevent a completed recommendation even though the agent now stops with an
actionable message. The evaluation also covers the five fixed scenarios rather
than every listing category or phrasing. A future test could apply the stricter
exact-title/two-detail check across several different selected items.

I stopped after this one measured prompt change because Milestone 5 requires a
single intervention; another behavior change would make the Before/After
effect impossible to attribute to one cause.

---

## Bonus — Second Measured Improvement

**Diagnosis:** The earlier empty-search loop stopped immediately when an
explicit size filter produced no matches. The failure place was the loop
branch, and the mechanism was that it treated the first `[]` as final without
checking whether size alone was the restrictive constraint.

**One change:** In `agent.py::run_agent`, a sized search that returns `[]` now
retries exactly once with `size=None`. Session state records the original size
in `dropped_constraints`, the trace names that dropped value, and a second
empty result still stops before `suggest_outfit`.

**Isolation:** The same five scenarios, criteria, targets, model settings, and
cache-off evaluator were used. This run occurred before moving the second tool
onto MCP, so the comparison measures only the retry change.

### Run Log — Bonus Retry

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | At least 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item stays the same across session state | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes the selected item and a styling detail | At least 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe returns general styling advice without an error | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

The complete unedited output for all 25 Bonus Retry tries is in
`results/run_2026-10-06_2344_bonus_retry.md`. The evidence below is copied
from Try 1 of each scenario.

#### Criterion 1 evidence — Bonus Retry

Source: `agent.py` — `run_agent()`; captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:

Channeling major early 2000s energy in this Y2K Baby Tee — Butterfly Print paired with baggy straight-leg jeans and chunky white sneakers. Score this vintage piece for just $18.00 on Depop before it’s gone!

Trace:

[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear Contrast** * **Top:** Y2K Baby Tee — Butterfly Print * **Bottoms:** Baggy straight-…
[3] create_fit_card
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear Contrast**\n* **Top:** Y2K Baby …
      out: Channeling major early 2000s energy in this Y2K Baby Tee — Butterfly Print paired with baggy straight-leg jean…
```

#### Criterion 2 evidence — Bonus Retry

Source: `agent.py` — `run_agent()`; captured by `run_eval.py` — `run_once()`

```text
- stopped early: yes — No listings matched even after retrying without the size filter 'XXS'. Try using different description words or raising the maximum price.
- selected_item: (none)
- search_results: 0

Trace:

[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, retrying once without the size filter (dropped size='XXS')
[2] search_listings (via MCP)
      in:  description='designer ballgown', size=None, max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping
```

#### Criterion 3 evidence — Bonus Retry

Source: `agent.py` — `run_agent()`; captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 7

[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe' (id=lst_004), wardrobe_items=10
      out: **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Outerwear:** 90s Track Jacket (Navy/W…
```

#### Criterion 4 evidence — Bonus Retry

Source: `tools.py` — `create_fit_card()` via `agent.py` — `run_agent()`;
captured by `run_eval.py` — `run_once()`

```text
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)

Outfit suggestion:

**Outfit 1: High-Contrast Denim (Double Denim)**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Denim jacket (light wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

Fit card:

Canadian tuxedo, but make it high-contrast. I threw this Denim Jacket — Light Wash, Cropped over a fitted white tank and dark baggy jeans for the ultimate casual streetwear vibe. Snagged it for $42.00 on Poshmark and honestly, it’s the best blank canvas.
```

#### Criterion 5 evidence — Bonus Retry

Source: `tools.py` — `suggest_outfit()` via `agent.py` — `run_agent()`;
captured by `run_eval.py` — `run_once()`

```text
- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

Buy it. At $42 with structured shoulders, this light wash cropped denim jacket is a versatile layering staple.

Here are two ways to style it using common basics:

1. **Casual Contrast:** Pair it over a fitted black ribbed tank top with high-waisted wide-leg black trousers and white leather sneakers. The structured shoulders will elevate a simple monochrome base.
2. **Double Denim / Textures:** Wear it over a simple white crewneck t-shirt tucked into olive green cargo pants or pleated beige chinos, finished with canvas slip-on shoes.

[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=0
      out: Buy it. At $42 with structured shoulders, this light wash cropped denim jacket is a versatile layering staple.…
```

### Successful looser-constraint retry

Command:
`python app.py ask 'denim jacket size XXS under $50' --trace`

```text
[1] search_listings (via MCP)
      in:  description='denim jacket', size='XXS', max_price=50.0
      out: [] (empty)
      →    branch: empty, retrying once without the size filter (dropped size='XXS')
[2] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[3] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=10
      out: **Verdict:** Buy. It pairs seamlessly with your existing basics and provides a lighter outerwear option than y…
[4] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Verdict:** Buy. It pairs seamlessly with your existin…
      out: Found the ultimate layering piece with this Denim Jacket — Light Wash, Cropped for just $42 on Poshmark. I lov…
```

**Did the second improvement help:** It improved the sized-search behavior but
made no numerical difference to the original criteria: After and Bonus Retry
were both 5 of 5 on all five rows. The new behavior is demonstrated directly:
all five Criterion 2 tries logged the one size-free retry before stopping, and
the separate valid-budget trace recovered seven listings and completed the
remaining tools.

---

## Bonus — Second Tool on MCP

**Tool moved:** `create_fit_card(outfit, new_item)` is now registered beside
`search_listings` in `mcp_server.py`.

**Code path:** `agent.py::run_agent` → `mcp_client.call_tool` →
`mcp_server.py::create_fit_card` → `tools.py::create_fit_card`. The MCP client
unwraps the result back to `str`, so the logical fit-card value stored in
session did not change; only its call path changed. `suggest_outfit` remains a
direct call.

**Server tool listing:** `python mcp_client.py`

```text
Asking mcp_server.py what it offers…

  search_listings
    Return ranked listing dictionaries matching the description, optional size, and inclusive maximum price, or [] when nothing matches.
    - description: string
    - size: string  (optional)
    - max_price: number  (optional)

  create_fit_card
    Return a short social caption based on an outfit suggestion and its selected listing.
    - outfit: string
    - new_item: object
```

**Direct MCP return-shape check:**

```text
RETURN_TYPE=str
Nothing beats finding the exact Vintage Levi's 501 Jeans — Medium Wash I've been hunting for. Grabbed these on Depop for just $38.00 and they fit like an absolute dream. I'm wearing them with a simple white ribbed tank and chunky white sneakers for the ultimate effortless weekend vibe.
```

**Full agent run through both MCP paths:**
`python app.py ask 'vintage graphic tee under $30' --trace`

```text
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear** *   **Top:** Y2K Baby Tee — Butterfly Print *   **Bottoms:** Baggy straight-leg j…
[3] create_fit_card (via MCP)
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear**\n*   **Top:** Y2K Baby Tee — B…
      out: Channeling ultimate early 2000s energy in this Y2K Baby Tee — Butterfly Print. I’m styling it with baggy strai…
```

This MCP move was made after the Bonus Retry evaluation, so it does not affect
the attribution of the second measured improvement.


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
