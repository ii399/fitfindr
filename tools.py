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

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

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
   # Step 1: Load all available clothing listings
    listings = load_listings()

    # Step 2a: Filter by maximum price, if provided
    if max_price is not None:
        listings = [
            item for item in listings
            if item["price"] <= max_price
        ]

    # Step 2b: Filter by size, if provided
    if size is not None:
        requested_size = size.strip().upper()

        filtered = []

        for item in listings:
            listing_size = item["size"].upper()

            # Remove parenthetical notes, such as "(oversized)"
            listing_size = listing_size.split("(")[0].strip()

            if requested_size in {"S", "M", "L", "XL"}:
                # Match complete size components, not substrings
                size_options = [
                    part.strip()
                    for part in listing_size.split("/")
                ]

                if requested_size in size_options:
                    filtered.append(item)

            elif requested_size.startswith("W"):
                # Match waist size, e.g. W30 or W30 L30
                if requested_size == listing_size.split()[0]:
                    filtered.append(item)

            else:
                # Exact match for shoe sizes and other formats
                if requested_size == listing_size:
                    filtered.append(item)

        listings = filtered

    # Step 3: Score listings by keyword overlap
    keywords = description.lower().split()

    scored_listings = []

    for item in listings:
        searchable_text = " ".join([
            item["title"],
            item["description"],
            item["category"],
            " ".join(item["style_tags"]),
            " ".join(item["colors"]),
            item["brand"] or ""
        ]).lower()

       # Give title matches more importance
        title_words = item["title"].lower().split()
        all_words = searchable_text.split()

        score = sum(
            3 if keyword in title_words
            else 1 if keyword in all_words
            else 0
            for keyword in keywords
        )

        # Step 4: Exclude listings with no keyword matches
        if score > 0:
            scored_listings.append((score, item))

        # Sort by relevance, highest score first
        scored_listings.sort(key=lambda result: result[0], reverse=True)

    return [
        item for score, item in scored_listings[:config.SEARCH_RESULT_LIMIT]
    ]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

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

    # Step 1: Get the wardrobe items
    wardrobe_items = wardrobe.get("items", [])

    # Step 2: Check whether the wardrobe is empty
    if not wardrobe_items:
        prompt = f"""
        You are a helpful fashion stylist.

        A user is considering buying this thrifted item:
        Name: {new_item['title']}
        Description: {new_item['description']}
        Color: {', '.join(new_item['colors'])}
        Style: {', '.join(new_item['style_tags'])}

        The user has not provided any wardrobe items.

        Suggest one or two ways to style this item using general
        clothing recommendations.

        Do not claim the user already owns any suggested clothing.
        Keep your suggestions practical, clear, and concise.
        """

        return generate(prompt)

    # Step 3: Format the user's wardrobe items
    wardrobe_lines = []

    for item in wardrobe_items:
        item_description = (
            f"- {item['name']} "
            f"(Category: {item['category']}, "
            f"Colors: {', '.join(item['colors'])}, "
            f"Styles: {', '.join(item['style_tags'])})"
        )

        if item.get("notes"):
            item_description += f" Notes: {item['notes']}"

        wardrobe_lines.append(item_description)

    wardrobe_text = "\n".join(wardrobe_lines)

    # Step 4: Ask the AI model for outfit suggestions
    prompt = f"""
    You are a helpful fashion stylist.

    The user is considering buying this thrifted item:
    Name: {new_item['title']}
    Description: {new_item['description']}
    Colors: {', '.join(new_item['colors'])}
    Styles: {', '.join(new_item['style_tags'])}

    The user already owns these wardrobe items:
    {wardrobe_text}

    Suggest one or two complete outfits combining the new item
    with specific pieces from the user's existing wardrobe.

    Use the exact names of wardrobe pieces where possible.
    Do not invent items that are not in the wardrobe.
    Explain briefly why the combinations work.
    Keep your response practical and concise.
    """

    return generate(prompt)


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

   # Step 1: Handle an empty or whitespace-only outfit
    if not outfit or not outfit.strip():
        return "A fit card cannot be created because no outfit suggestion was provided."

    # Step 2: Build the AI prompt
    prompt = f"""
    You are creating a short, engaging social media caption
    for a thrifted fashion find.

    Selected item:
    Name: {new_item['title']}
    Price: ${float(new_item['price']):.2f}
    Platform: {new_item['platform']}
    Description: {new_item['description']}
    Style tags: {', '.join(new_item['style_tags'])}

    Outfit suggestion:
    {outfit}

    Write a caption that:
    1. Contains 2 to 4 sentences.
    2. Mentions the item's exact name once.
    3. Mentions its price once.
    4. Mentions the selling platform once.
    5. Describes the outfit's specific style or vibe.
    6. Sounds like a real social media post, not a product description.
    7. Display the price exactly as provided, including two decimal places.
    8. Preserve the selling platform's capitalization exactly as provided.
    
    Return only the caption.
    """

    # Step 3: Generate and return the caption
    return generate(prompt)
