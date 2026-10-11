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

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches clothing listings for items matching the user's description, optional size, and maximum price.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" --> 
`description` (str), `size` (str or None), `max_price` (float or None).
- **Returns:**  A list of matching listing dictionaries (`list[dict]`), each containing fields such as `id`, `title`, `price`, `size`, `style_tags`, and `platform`, sorted by relevance.
- **When it has nothing:** Returns an empty list (`[]`) when no matching clothing items are found.

**Size-matching rules:** Size matching is case-insensitive. Letter sizes (`S`, `M`, `L`, `XL`) match exact size components, including combined sizes such as `S/M` and `M/L`. Waist sizes match the first size component, so `W30` matches both `W30` and `W30 L30`. Shoe sizes require an exact match, so `US 8` does not match `US 8.5`. Parenthetical size notes are ignored when matching. One-size items are not automatically included in searches for letter sizes.

### `suggest_outfit`

- **What it does:** Suggests an outfit by combining a selected clothing item with pieces from the user's existing wardrobe.
- **Inputs:** `new_item` (dict) — the selected clothing listing; `wardrobe` (dict) — the user's wardrobe containing an `items` list.
- **Returns:** A string (`str`) describing how to style the selected item with specific clothing pieces from the user's wardrobe.
- **When it has nothing:** If the wardrobe is empty, returns general styling advice for the selected item instead of failing.

### `create_fit_card`

- **What it does:** Generates a short, engaging fit card describing the suggested outfit and selected clothing item.
- **Inputs:** `outfit` (str) — the outfit suggestion; `new_item` (dict) — the selected clothing listing.
- **Returns:** A string (`str`) containing a two-to-four-sentence caption describing the outfit's style and mentioning the selected item's name, price, and platform.
- **When it has nothing:** If the outfit suggestion is empty, returns an explanatory message instead of generating a fit card.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

If `search_listings` returns an empty list (`[]`), save a helpful
message in `session["error"]` explaining that no listings matched
and suggesting what the user can change, then stop without calling
`suggest_outfit`.

Otherwise, take the first listing from the search results, save it
in `session["selected_item"]`, and pass that selected item to
`suggest_outfit` along with the user's wardrobe. Save the outfit
suggestion in `session["outfit_suggestion"]`, then pass it and the
selected item to `create_fit_card`.


**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

### Tool 1: search_listings — Independent Test

**Command:**

```powershell
python -c "from tools import search_listings; results = search_listings('designer ballgown', size='XXS', max_price=5); print('Results:', results); print('Is empty list:', results == [])"
```
**Terminal output:**

```text
Results: []
Is empty list: True
```

**Observation:**

The search returned an empty list when no clothing matched the requested description, size, and budget. This confirms that the tool handles an unsuccessful search without returning an exception or `None`.

### Tool 2: suggest_outfit — Independent Test

**Command:**

```powershell
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; result = suggest_outfit(load_listings()[0], get_example_wardrobe()); print(result)"
```
**Terminal output:**

```text
As your stylist, I definitely recommend grabbing these Vintage Levi's 501 Jeans—they are a timeless staple that will add a great relaxed, authentic texture to your closet. 

Here are two complete outfits combining the new jeans with pieces you already own:

### Outfit 1: Casual Streetwear
* **Top:** White ribbed tank top
* **Outerwear:** Vintage black denim jacket
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Why it works:** 
The fitted white tank balances the straight-leg cut of the vintage 501s, while the slightly cropped black denim jacket creates a cool, layered denim-on-denim look. Finished with the chunky white sneakers andcrossbody bag, this is an effortless, everyday outfit with a classic streetwear edge.

### Outfit 2: Cozy & Grunge-Influenced
* **Top:** Oversized grey crewneck sweatshirt
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt

**Why it works:** 
Tucking the front of the oversized grey crewneck into the 501s highlights the waist while keeping that cozy, relaxed vibe. Pairing the medium wash denim with the black combat boots adds a subtle grunge contrast, and the brown leather belt pulls the whole casual look together.
```

**Observation:**

The tool generated two outfit suggestions using the selected Levi's jeans and named specific items from the example wardrobe. It also explained why each combination works.

### Tool 3: create_fit_card — Independent Test

**Command:**

```powershell
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
```

**Terminal output:**

```text
Nothing beats the effortless, off-duty streetwear vibe of these Vintage Levi's 501 Jeans — Medium Wash with their perfectly worn-in knees. Just style them with your favorite crisp white sneakers for that timeless, everyday look. Grab this classic pair now on depop for $38.00 before someone else does! #vintage #classic #denim #streetwear
```

**Observation:**

The tool generated a three-sentence cdoneaption mentioning the selected Levi's jeans, their $38.00 price, the Depop platform, and the outfit's streetwear vibe. Three additional runs with caching disabled produced different captions while preserving the required information. The model did not consistently preserve the platform's capitalization.

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

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
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

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

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



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
