# Run log — bonus_retry

- Produced by: `run_eval.py::main`
- Loop: `agent.py::run_agent` · tools: `tools.py`
- Tries per scenario: 5, caching off
- Temperature: 0.9
- When: 2026-10-06 23:44

Paste the table below into your README. Fill in the Criterion and
Target columns from `criteria.md`, then mark each try PASS or FAIL
from the output underneath and count them for the Verdict.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes |  |   |   |   |   |   |  |
| 2. impossible query stops early |  |   |   |   |   |   |  |
| 3. selected item survives session handoff |  |   |   |   |   |   |  |
| 4. fit card preserves item and styling detail |  |   |   |   |   |   |  |
| 5. empty wardrobe returns general advice |  |   |   |   |   |   |  |

> The Try and Verdict columns are blank on purpose. Whether a try
> passed depends on the criterion you wrote, so it's yours to decide.
> Count the passes, then read that count against your target: a row
> targeting 4 of 5 with three PASS cells is MISSED (3/5).

---

## What actually happened

Real output, as text. Paste the relevant parts into your README —
the rubric asks for output, not a description of it.

### matching query completes

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear Contrast**
* **Top:** Y2K Baby Tee — Butterfly Print
* **Bottoms:** Baggy straight-leg jeans (dark blue/indigo)
* **Outerwear:** Vintage black denim jacket
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Why it works:** The fitted crop of the baby tee balances the volume of the high-waisted baggy jeans, nailing the Y2K silhouette. Layering the slightly cropped black denim jacket keeps the proportions sharp, while the chunky white sneakers tie into the white graphic on the tee.

***

**Outfit 2: Casual Retro Mix**
* **Top:** Y2K Baby Tee — Butterfly Print
* **Bottoms:** Wide-leg khaki trousers
* **Shoes:** Chunky white sneakers
* **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** Pairing the ultra-feminine pink and purple butterfly tee with tailored wide-leg khakis creates an effortless "high-low" mix of Y2K and minimal streetwear. The brown leather belt adds a grounding neutral touch, and the white sneakers keep the look relaxed and grounded.
```

Fit card:

```
Channeling major early 2000s energy in this Y2K Baby Tee — Butterfly Print paired with baggy straight-leg jeans and chunky white sneakers. Score this vintage piece for just $18.00 on Depop before it’s gone!
```

Trace:

```
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

**Try 2**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear**
*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark blue)
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The fitted, cropped silhouette of the baby tee balances the volume of the high-waisted, baggy dark wash jeans for a classic Y2K proportion. Adding the slightly cropped black denim jacket and chunky white sneakers ties the streetwear theme together while keeping the color palette grounded.

***

**Outfit 2: Casual Contrast**
*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Shoes:** Chunky white sneakers

**Why it works:** Pairing the hyper-feminine, fitted pink and purple butterfly tee with tailored, wide-leg khaki trousers creates a balanced high-low mix. The brown leather belt adds definition at the waist, and the white sneakers keep the look grounded and casual.
```

Fit card:

```
Nothing beats finding the ultimate Y2K Baby Tee — Butterfly Print while rummaging through the racks. I’m styling this $18.00 find with baggy straight-leg jeans and chunky white sneakers for the perfect off-duty streetwear vibe. Grab it now on Depop before I change my mind!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear** *   **Top:** Y2K Butterfly Baby Tee *   **Bottoms:** Baggy straight-leg jeans (da…
[3] create_fit_card
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear**\n*   **Top:** Y2K Butterfly Ba…
      out: Nothing beats finding the ultimate Y2K Baby Tee — Butterfly Print while rummaging through the racks. I’m styli…
```

**Try 3**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear**
*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark blue)
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The fitted, cropped silhouette of the baby tee balances the volume of the high-waisted baggy jeans, creating a classic Y2K proportion. Adding the slightly cropped black denim jacket and chunky white sneakers ties the streetwear theme together while keeping the color palette grounded.

***

**Outfit 2: Casual Contrast**
*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Black cropped zip hoodie (worn open or carried)
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, black crossbody bag

**Why it works:** Pairing the ultra-feminine, pastel butterfly tee with utilitarian khaki trousers and edgy black combat boots creates a high-low mix of styles. The fitted top tucks neatly into the wide-leg trousers to define your waist.
```

Fit card:

```
Channeling total 2000s energy in this Y2K Baby Tee — Butterfly Print. I love pairing it with baggy straight-leg jeans and chunky white sneakers for the ultimate nostalgic streetwear vibe. Grab it on Depop for just $18.00 before it’s gone!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear** *   **Top:** Y2K Butterfly Baby Tee *   **Bottoms:** Baggy straight-leg jeans (da…
[3] create_fit_card
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear**\n*   **Top:** Y2K Butterfly Ba…
      out: Channeling total 2000s energy in this Y2K Baby Tee — Butterfly Print. I love pairing it with baggy straight-le…
```

**Try 4**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear**
*   **Top:** Y2K baby tee ($18)
*   **Bottoms:** Baggy straight-leg jeans
*   **Outerwear:** Vintage black denim jacket 
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The fitted, cropped silhouette of the baby tee balances the volume of the high-waisted baggy jeans, creating a classic Y2K proportion. Adding the slightly cropped black denim jacket and chunky white sneakers ties the streetwear aesthetic together.

***

**Outfit 2: Casual Contrast**
*   **Top:** Y2K baby tee ($18)
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** This pairs the ultra-feminine, pink-and-purple butterfly tee with structured, minimal khaki trousers for a high-low mix. The chunky white sneakers keep the look grounded and casual.
```

Fit card:

```
Channeling ultimate 2000s energy with this Y2K Baby Tee — Butterfly Print for just $18 on depop. I love styling it with baggy straight-leg jeans and chunky white sneakers for that classic Y2K streetwear proportion. It gives off such a fun, nostalgic vibe that’s super easy to throw on and go!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear** *   **Top:** Y2K baby tee ($18) *   **Bottoms:** Baggy straight-leg jeans *   **O…
[3] create_fit_card
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear**\n*   **Top:** Y2K baby tee ($1…
      out: Channeling ultimate 2000s energy with this Y2K Baby Tee — Butterfly Print for just $18 on depop. I love stylin…
```

**Try 5**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear Contrast**
*   **Top:** Y2K Baby Tee (Butterfly Print)
*   **Bottoms:** Baggy straight-leg jeans (dark blue)
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The fitted, cropped cut of the baby tee balances the volume of the high-waisted baggy jeans, nailing the Y2K silhouette. Layering the slightly cropped black denim jacket and adding chunky white sneakers completes the 2000s streetwear aesthetic.

***

**Outfit 2: Casual Retro Minimal**
*   **Top:** Y2K Baby Tee (Butterfly Print)
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Shoes:** Chunky white sneakers

**Why it works:** Tucking the baby tee into the high-waisted wide-leg khaki trousers creates a clean contrast between the pink and purple graphic and the neutral tan base. The brown leather belt ties the earth tones together while keeping the proportions sharp.
```

Fit card:

```
Channeling total 2000s icon energy in this Y2K Baby Tee — Butterfly Print paired with baggy dark wash jeans and chunky white sneakers. It's giving effortless streetwear contrast and I'm obsessed. Grab it on Depop for just $18.00 before it's gone!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print' (id=lst_002), wardrobe_items=10
      out: **Outfit 1: Y2K Streetwear Contrast** *   **Top:** Y2K Baby Tee (Butterfly Print) *   **Bottoms:** Baggy strai…
[3] create_fit_card
      in:  new_item='Y2K Baby Tee — Butterfly Print'; outfit='**Outfit 1: Y2K Streetwear Contrast**\n*   **Top:** Y2K Bab…
      out: Channeling total 2000s icon energy in this Y2K Baby Tee — Butterfly Print paired with baggy dark wash jeans an…
```

### impossible query stops early

- Query: `designer ballgown size XXS under $5`
- Wardrobe: example

**Try 1**

- stopped early: yes — No listings matched even after retrying without the size filter 'XXS'. Try using different description words or raising the maximum price.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, retrying once without the size filter (dropped size='XXS')
[2] search_listings (via MCP)
      in:  description='designer ballgown', size=None, max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping
```

**Try 2**

- stopped early: yes — No listings matched even after retrying without the size filter 'XXS'. Try using different description words or raising the maximum price.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, retrying once without the size filter (dropped size='XXS')
[2] search_listings (via MCP)
      in:  description='designer ballgown', size=None, max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping
```

**Try 3**

- stopped early: yes — No listings matched even after retrying without the size filter 'XXS'. Try using different description words or raising the maximum price.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, retrying once without the size filter (dropped size='XXS')
[2] search_listings (via MCP)
      in:  description='designer ballgown', size=None, max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping
```

**Try 4**

- stopped early: yes — No listings matched even after retrying without the size filter 'XXS'. Try using different description words or raising the maximum price.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, retrying once without the size filter (dropped size='XXS')
[2] search_listings (via MCP)
      in:  description='designer ballgown', size=None, max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping
```

**Try 5**

- stopped early: yes — No listings matched even after retrying without the size filter 'XXS'. Try using different description words or raising the maximum price.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, retrying once without the size filter (dropped size='XXS')
[2] search_listings (via MCP)
      in:  description='designer ballgown', size=None, max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping
```

### selected item survives session handoff

- Query: `90s track jacket in size M`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top
*   **Outerwear:** 90s Track Jacket (Navy/White Stripe)
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The fitted white tank balances the volume of the baggy dark jeans, while the navy track jacket adds a sporty, authentic 90s layer. Finishing with chunky white sneakers ties the athletic and streetwear aesthetic together.

***

**Outfit 2: High-Low Mix**
*   **Top:** White ribbed tank top
*   **Outerwear:** 90s Track Jacket (Navy/White Stripe)
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** Pairing the athletic navy track jacket with tailored khaki trousers creates a deliberate high-low contrast. The white tank keeps the base clean, and the black combat boots ground the lighter tones of the pants and jacket.
```

Fit card:

```
Nothing beats throwing on a 90s Track Jacket — Navy/White Stripe over a fitted white tank and baggy jeans for that effortless streetwear vibe. I scored this authentic vintage layer for $45.00 on Poshmark, and it honestly goes with everything. Grab it before I change my mind!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='90s track jacket', size='M', max_price=None
      out: 7 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe' (id=lst_004), wardrobe_items=10
      out: **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Outerwear:** 90s Track Jacket (Navy/W…
[3] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe'; outfit='**Outfit 1: Casual Streetwear**\n*   **Top:** White r…
      out: Nothing beats throwing on a 90s Track Jacket — Navy/White Stripe over a fitted white tank and baggy jeans for …
```

**Try 2**

- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans (dark blue/indigo)
*   **Outerwear:** 90s Track Jacket (navy/white)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   **Why it works:** Pairing the track jacket with the white ribbed tank and baggy jeans leans directly into an effortless 90s streetwear aesthetic. The chunky white sneakers tie in with the white stripe on the jacket, and the crossbody bag keeps it practical and minimal.

**Outfit 2: High-Low Athletic Minimal**
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** 90s Track Jacket (navy/white)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Why it works:** This mixes sporty and tailored elements. The crisp navy-and-white jacket dresses down the sharp khaki trousers for a balanced, modern look. The brown belt adds a warm neutral contrast, and the white sneakers anchor the athletic vibe.
```

Fit card:

```
Channeling peak 90s streetwear with this 90s Track Jacket — Navy/White Stripe. I love throwing it on over a ribbed tank with baggy jeans and chunky white sneakers for the ultimate effortless look. Snagged this vintage find on Poshmark for just $45.00!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='90s track jacket', size='M', max_price=None
      out: 7 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe' (id=lst_004), wardrobe_items=10
      out: **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy straight-leg jeans (…
[3] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe'; outfit='**Outfit 1: Casual Streetwear**\n*   **Top:** White r…
      out: Channeling peak 90s streetwear with this 90s Track Jacket — Navy/White Stripe. I love throwing it on over a ri…
```

**Try 3**

- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top
*   **Outerwear:** 90s Track Jacket (Navy/White Stripe)
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** Pairing the lightweight track jacket with the fitted white tank creates a balanced silhouette, while the dark wash baggy jeans and chunky sneakers lean into the 90s streetwear aesthetic. 

***

**Outfit 2: High-Low Sporty Minimalist**
*   **Top:** White ribbed tank top
*   **Outerwear:** 90s Track Jacket (Navy/White Stripe)
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Brown leather belt

**Why it works:** The tailored wide-leg trousers tone down the athletic feel of the track jacket for a modern, high-low look. Tucking in the white tank and adding the belt pulls the separates together cleanly.
```

Fit card:

```
Channeling the ultimate 90s streetwear vibe with this 90s Track Jacket — Navy/White Stripe layered over a white ribbed tank and baggy jeans. Throw on some chunky sneakers to complete the look. Snagged this vintage piece on Poshmark for just $45.00!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='90s track jacket', size='M', max_price=None
      out: 7 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe' (id=lst_004), wardrobe_items=10
      out: **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Outerwear:** 90s Track Jacket (Navy/W…
[3] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe'; outfit='**Outfit 1: Casual Streetwear**\n*   **Top:** White r…
      out: Channeling the ultimate 90s streetwear vibe with this 90s Track Jacket — Navy/White Stripe layered over a whit…
```

**Try 4**

- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top
*   **Outerwear:** 90s track jacket (Navy/White Stripe)
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The fitted white tank balances the volume of the baggy dark wash jeans. Layering the navy track jacket on top plays into the 90s streetwear aesthetic, and the chunky white sneakers tie the white stripe details of the jacket together.

***

**Outfit 2: Sporty Smart-Casual**
*   **Top:** White ribbed tank top
*   **Outerwear:** 90s track jacket (Navy/White Stripe)
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** Pairing the athletic track jacket with tailored khaki trousers creates a high-low mix. Tucking in the white tank with the brown belt anchors the earth tones of the trousers, while the white sneakers keep the sporty theme cohesive.
```

Fit card:

```
Nothing beats the effortless streetwear vibe of this 90s Track Jacket — Navy/White Stripe. I love layering it over a white ribbed tank with baggy dark wash jeans and chunky sneakers. Grab this vintage find for $45.00 on Poshmark before I change my mind!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='90s track jacket', size='M', max_price=None
      out: 7 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe' (id=lst_004), wardrobe_items=10
      out: **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Outerwear:** 90s track jacket (Navy/W…
[3] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe'; outfit='**Outfit 1: Casual Streetwear**\n*   **Top:** White r…
      out: Nothing beats the effortless streetwear vibe of this 90s Track Jacket — Navy/White Stripe. I love layering it …
```

**Try 5**

- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: Casual Streetwear**
* **Top:** White ribbed tank top
* **Bottoms:** Baggy straight-leg jeans (dark blue)
* **Outerwear:** 90s track jacket (navy/white)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

*Why it works:* Pairing the sporty track jacket over a fitted white tank and baggy denim leans directly into the 90s streetwear aesthetic. The chunky white sneakers tie the white accents of the jacket together for a cohesive, effortless look.

***

**Outfit 2: High-Low Sporty Minimal**
* **Bottoms:** Wide-leg khaki trousers
* **Outerwear:** 90s track jacket (navy/white)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag *(optional: leave the white tank underneath unmentioned if worn unzipped, or layer it underneath)*

*Why it works:* This outfit contrasts the casual, athletic energy of the track jacket with the tailored structure of wide-leg khaki trousers. Finishing with chunky white sneakers keeps the outfit grounded in a modern, comfortable style.
```

Fit card:

```
Leaning all the way into that effortless 90s streetwear vibe with this vintage 90s Track Jacket — Navy/White Stripe. I love throwing it over a fitted white tank with baggy dark denim and chunky sneakers. Grab it on Poshmark for $45!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='90s track jacket', size='M', max_price=None
      out: 7 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe' (id=lst_004), wardrobe_items=10
      out: **Outfit 1: Casual Streetwear** * **Top:** White ribbed tank top * **Bottoms:** Baggy straight-leg jeans (dark…
[3] create_fit_card
      in:  new_item='90s Track Jacket — Navy/White Stripe'; outfit='**Outfit 1: Casual Streetwear**\n* **Top:** White rib…
      out: Leaning all the way into that effortless 90s streetwear vibe with this vintage 90s Track Jacket — Navy/White S…
```

### fit card preserves item and styling detail

- Query: `denim jacket under $50`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: High-Contrast Denim (Double Denim)**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Denim jacket (light wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   **Why it works:** The light wash of the jacket contrasts sharply against the dark indigo jeans, breaking up the double-denim look. The fitted white tank balances the volume of the baggy bottoms and the cropped jacket length highlights your waist. 

**Outfit 2: Casual Earth Tones**
*   **Top:** Oversized grey crewneck sweatshirt (worn underneath) 
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Denim jacket (light wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Why it works:** Layering the oversized grey crewneck under the structured, cropped light wash jacket creates a balanced play of proportions. The khaki trousers and brown belt ground the cool-toned grey and blue with warm, neutral earth tones.
```

Fit card:

```
Canadian tuxedo, but make it high-contrast. I threw this Denim Jacket — Light Wash, Cropped over a fitted white tank and dark baggy jeans for the ultimate casual streetwear vibe. Snagged it for $42.00 on Poshmark and honestly, it’s the best blank canvas.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=10
      out: **Outfit 1: High-Contrast Denim (Double Denim)** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy str…
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Outfit 1: High-Contrast Denim (Double Denim)**\n*   *…
      out: Canadian tuxedo, but make it high-contrast. I threw this Denim Jacket — Light Wash, Cropped over a fitted whit…
```

**Try 2**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: High-Contrast Denim (Double Denim)**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Denim jacket (light wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** Pairing the light wash cropped jacket with dark indigo baggy jeans creates a balanced high-contrast double-denim look. The cropped length of the jacket accentuates the high waist of the jeans, while the fitted white tank and chunky white sneakers keep the outfit grounded and casual.

***

**Outfit 2: Streetwear Layering**
*   **Top:** Black cropped zip hoodie
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Denim jacket (light wash)
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

**Why it works:** Layering the light denim jacket over the black cropped zip hoodie adds dimension and a streetwear edge to the minimal khaki trousers. The structured shoulders of the jacket balance the volume of the wide-leg pants, and the black combat boots tie the heavier pieces together.
```

Fit card:

```
Thrifted this perfect Denim Jacket — Light Wash, Cropped for just $42.00 on Poshmark. I love throwing it on over a black cropped zip hoodie with wide-leg khaki trousers for an effortless streetwear vibe. It has the best structured shoulders and is ready for everyday layering.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=10
      out: **Outfit 1: High-Contrast Denim (Double Denim)** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy str…
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Outfit 1: High-Contrast Denim (Double Denim)**\n*   *…
      out: Thrifted this perfect Denim Jacket — Light Wash, Cropped for just $42.00 on Poshmark. I love throwing it on ov…
```

**Try 3**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: Double Denim Contrast**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans (dark blue/indigo)
*   **Outerwear:** Cropped light wash denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The light wash of the new jacket creates a sharp contrast against your dark wash, high-waisted jeans, visually breaking up a double-denim look. The cropped length of the jacket hits right where the jeans sit, accentuating your waist, while the white tank and sneakers tie the casual streetwear vibe together.

***

**Outfit 2: High-Contrast Casual**
*   **Top:** White ribbed tank top
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Cropped light wash denim jacket
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** Pairing light blue denim with tan khaki trousers creates a clean, classic color palette. Tucking in the white tank with the brown belt defines your waist, and the cropped jacket keeps the proportions balanced over the wide-leg pants. The black combat boots add a grounded, edgy finish.
```

Fit card:

```
Mastering double denim is easy with this vintage-vibed Denim Jacket — Light Wash, Cropped paired over dark baggy jeans and chunky white sneakers. I love the structured shoulders, and it’s a total steal for $42.00 on Poshmark. Throw on a white ribbed tank and you've got the ultimate casual streetwear fit.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=10
      out: **Outfit 1: Double Denim Contrast** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy straight-leg jea…
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Outfit 1: Double Denim Contrast**\n*   **Top:** White…
      out: Mastering double denim is easy with this vintage-vibed Denim Jacket — Light Wash, Cropped paired over dark bag…
```

**Try 4**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: High-Contrast Denim (Canadian Tuxedo)**
* **Top:** White ribbed tank top
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Outerwear:** Light wash cropped denim jacket (new item)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Why it works:** The cropped cut of the light wash jacket hits right at the waist of your high-waisted dark jeans, creating a flattering proportion. The sharp contrast between the light and dark denim keeps the double-denim look modern, while the fitted white tank and white sneakers tie the light elements together. 

***

**Outfit 2: Streetwear Casual**
* **Top:** Black cropped zip hoodie (layered under the jacket)
* **Bottoms:** Wide-leg khaki trousers
* **Outerwear:** Light wash cropped denim jacket (new item)
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** Layering the black cropped zip hoodie under the structured shoulders of the light wash jacket adds depth and keeps you warm. The structured denim bridges the gap between the casual hoodie and tailored khaki trousers, and the black combat boots anchor the earthy tones of the outfit.
```

Fit card:

```
Channeling major off-duty streetwear vibes with this Denim Jacket — Light Wash, Cropped. I love layering it over a black cropped zip hoodie with wide-leg khaki trousers and combat boots for that effortless, textured look. Grab this blank canvas over on Poshmark for $42 before I change my mind!
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=10
      out: **Outfit 1: High-Contrast Denim (Canadian Tuxedo)** * **Top:** White ribbed tank top * **Bottoms:** Baggy stra…
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Outfit 1: High-Contrast Denim (Canadian Tuxedo)**\n* …
      out: Channeling major off-duty streetwear vibes with this Denim Jacket — Light Wash, Cropped. I love layering it ov…
```

**Try 5**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Outfit 1: High-Contrast Denim (Double Denim)**
*   **Top:** White ribbed tank top
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Light wash cropped denim jacket (new item)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** Pairing the light wash jacket with your dark wash baggy jeans creates a balanced two-tone denim look. The cropped cut of the jacket naturally hits above the high-waisted, dark indigo denim, defining your waist while keeping the overall silhouette relaxed and streetwear-inspired. 

**Outfit 2: Casual Earth Tones**
*   **Top:** White ribbed tank top
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Light wash cropped denim jacket (new item)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:** Light-wash denim pairs exceptionally well with tan and khaki. Tucking in the white tank and wearing the brown belt anchors the outfit, while the cropped jacket adds structure and keeps the wide-leg proportions from looking too heavy.
```

Fit card:

```
Obsessed with the structured shoulders on this Denim Jacket — Light Wash, Cropped. I styled it for a streetwear vibe with a white ribbed tank, baggy dark wash jeans, and chunky white sneakers. Grabbed it on Poshmark for $42.00 and it’s the ultimate blank canvas.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=10
      out: **Outfit 1: High-Contrast Denim (Double Denim)** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy str…
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Outfit 1: High-Contrast Denim (Double Denim)**\n*   *…
      out: Obsessed with the structured shoulders on this Denim Jacket — Light Wash, Cropped. I styled it for a streetwea…
```

### empty wardrobe returns general advice

- Query: `denim jacket under $50`
- Wardrobe: empty

**Try 1**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
Buy it. At $42 with structured shoulders, this light wash cropped denim jacket is a versatile layering staple. 

Here are two ways to style it using common basics:

1. **Casual Contrast:** Pair it over a fitted black ribbed tank top with high-waisted wide-leg black trousers and white leather sneakers. The structured shoulders will elevate a simple monochrome base.
2. **Double Denim / Textures:** Wear it over a simple white crewneck t-shirt tucked into olive green cargo pants or pleated beige chinos, finished with canvas slip-on shoes.
```

Fit card:

```
Scored this Denim Jacket — Light Wash, Cropped on Poshmark for just $42! I love throwing it over a fitted black ribbed tank with wide-leg trousers for that effortless, structured-shoulder look. Such a versatile vintage staple for building casual streetwear fits.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=0
      out: Buy it. At $42 with structured shoulders, this light wash cropped denim jacket is a versatile layering staple.…
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='Buy it. At $42 with structured shoulders, this light wa…
      out: Scored this Denim Jacket — Light Wash, Cropped on Poshmark for just $42! I love throwing it over a fitted blac…
```

**Try 2**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Verdict:** Buy. At $42, a structured, cropped light wash denim jacket is a versatile layering essential.

**Styling Recommendations:**
1. **Monochrome Base:** Pair it with a black fitted t-shirt or tank top, black high-waisted trousers, and white sneakers to let the light wash pop against a dark foundation.
2. **Casual Contrast:** Layer it over a simple white crewneck tee with olive green cargo pants and canvas slip-on shoes for an easy streetwear look.
```

Fit card:

```
Obsessed with the structured shoulders on this Denim Jacket — Light Wash, Cropped. Snagged it on Poshmark for $42 and I'm already planning to throw it over a black fitted tank and high-waisted trousers. It gives off the ultimate effortless streetwear vibe.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=0
      out: **Verdict:** Buy. At $42, a structured, cropped light wash denim jacket is a versatile layering essential.  **…
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Verdict:** Buy. At $42, a structured, cropped light w…
      out: Obsessed with the structured shoulders on this Denim Jacket — Light Wash, Cropped. Snagged it on Poshmark for …
```

**Try 3**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Verdict:** Buy. At $42, a structured, cropped light wash denim jacket is a versatile layering essential. 

**Two Ways to Style It Using Common Basics:**

1. **Casual Contrast:** Pair it over a fitted black ribbed tank top with high-waisted wide-leg black trousers and white leather sneakers. The cropped cut accentuates the waist against the relaxed pants.
2. **Monochrome Denim:** Layer it over a plain white crewneck t-shirt with straight-leg medium-wash jeans and black leather ankle boots, creating a balanced double-denim look.
```

Fit card:

```
Scored this sweet Denim Jacket — Light Wash, Cropped for just $42 on Poshmark. It has the best structured shoulders and is ready for everyday wear. I’m styling it with a fitted black ribbed tank and high-waisted wide-leg trousers for that effortless streetwear vibe.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=0
      out: **Verdict:** Buy. At $42, a structured, cropped light wash denim jacket is a versatile layering essential.   *…
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Verdict:** Buy. At $42, a structured, cropped light w…
      out: Scored this sweet Denim Jacket — Light Wash, Cropped for just $42 on Poshmark. It has the best structured shou…
```

**Try 4**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Recommendation 1: Casual Streetwear**
Layer the jacket over a plain white crewneck t-shirt and pair it with black straight-leg trousers and white leather sneakers. The structured shoulders add definition while the cropped length keeps the proportions balanced.

**Recommendation 2: Monochromatic Denim**
Wear the jacket over a black fitted ribbed tank top, paired with dark wash straight-leg jeans and black ankle boots. The light-wash crop will create sharp contrast against darker denim and shoes.
```

Fit card:

```
Found my new favorite layering piece! This Denim Jacket — Light Wash, Cropped is giving major effortless streetwear energy, especially thrown over a plain white tee and black straight-leg trousers. Grabbed it on Poshmark for just $42.00.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=0
      out: **Recommendation 1: Casual Streetwear** Layer the jacket over a plain white crewneck t-shirt and pair it with …
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Recommendation 1: Casual Streetwear**\nLayer the jack…
      out: Found my new favorite layering piece! This Denim Jacket — Light Wash, Cropped is giving major effortless stree…
```

**Try 5**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
**Buy it.** This is a versatile, foundational piece. 

Here are two ways to style it using common basics:

1. **Casual Everyday:** Pair it with a plain white t-shirt, black straight-leg trousers, and white leather sneakers. 
2. **Layered Contrast:** Throw it over a black ribbed midi dress with chunky black ankle boots to balance the cropped length.
```

Fit card:

```
Obsessed with this light wash Denim Jacket — Light Wash, Cropped I just scored on Poshmark for $42.00! It has the best structured shoulders and gives off such effortless streetwear energy. I'm totally planning to wear it over a black ribbed midi dress with chunky ankle boots for that ultimate high-low contrast.
```

Trace:

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    branch: results found, continuing
[2] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped' (id=lst_007), wardrobe_items=0
      out: **Buy it.** This is a versatile, foundational piece.   Here are two ways to style it using common basics:  1. …
[3] create_fit_card
      in:  new_item='Denim Jacket — Light Wash, Cropped'; outfit='**Buy it.** This is a versatile, foundational piece. \n…
      out: Obsessed with this light wash Denim Jacket — Light Wash, Cropped I just scored on Poshmark for $42.00! It has …
```
