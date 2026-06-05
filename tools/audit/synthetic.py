"""Synthetic identity pools for test fact generation.

Every value here is fictional. Real entity names, real registered-agent names,
and real CRA public numbers must never enter test cases -- both for correctness
(so a test never depends on live data) and for clean-room hygiene. The language
model proposes *scenario shape*; these pools supply the concrete identities
deterministically, indexed by a seed so runs are reproducible without
``random`` (which is unavailable in some sandboxes anyway).
"""

from __future__ import annotations

# Fictional Maine-flavored place/nature words to assemble entity names from.
_ROOTS = [
    "Wabanaki", "Downeast", "Casco Bay", "Katahdin", "Penobscot", "Allagash",
    "Kennebec", "Saco River", "Moosehead", "Acadia", "Rangeley", "Sebago",
    "Aroostook", "Damariscotta", "Boothbay", "Machias", "Norumbega", "Pemaquid",
]
_NATURES = [
    "Widgets", "Maritime Supply", "Timber Works", "Granite Holdings",
    "Lobster Co-op", "Cider Works", "Textile Mills", "Solar Collective",
    "Logistics", "Provisions", "Analytics", "Boatworks", "Creamery",
    "Trading Company", "Fabrication", "Robotics", "Press", "Outfitters",
]
_CORP_SUFFIX = ["Corporation", "Incorporated", "Company", "Corp.", "Inc."]
_LLC_SUFFIX = ["LLC", "L.L.C.", "Limited Liability Company"]
_LP_SUFFIX = ["LP", "L.P.", "Limited Partnership"]
_LLP_SUFFIX = ["LLP", "Registered Limited Liability Partnership"]
_NP_SUFFIX = ["Inc.", "Corporation", "Alliance", "Foundation", "Society"]

_FIRST = [
    "Avery", "Sage", "Rowan", "Quinn", "Marin", "Cole", "Reese", "Tamsin",
    "Ellery", "Wren", "Hollis", "Dax", "Frost", "Linden", "Oakley", "Briar",
]
_LAST = [
    "Stillwater", "Hawthorne", "Frostfield", "Marsh", "Birchall", "Coveney",
    "Ashford", "Pelletier", "Thibodeau", "Ouellette", "Gagnon", "Lessard",
    "Beaulieu", "Cyr", "Michaud", "Veilleux",
]
_AGENTS = [
    "Downeast Registered Agents, LLC", "Pine Tree Agent Services, Inc.",
    "Bay State Statutory Agents, LLC", "North Woods Compliance, LLC",
    "Harbor Registered Agents, Inc.",
]
_STREETS = [
    "12 Cove Road", "488 Granite Way", "7 Lighthouse Lane", "230 Mill Street",
    "94 Harbor Drive", "1500 Birch Hill Road", "61 Spruce Avenue",
]
_TOWNS = [
    ("Portland", "04101"), ("Bangor", "04401"), ("Augusta", "04330"),
    ("Bar Harbor", "04609"), ("Brunswick", "04011"), ("Camden", "04843"),
    ("Belfast", "04915"),
]

# Synthetic CRA public numbers. Real ones are state-assigned; these are clearly
# out-of-range placeholders for tests only.
_CRA_BASE = 90000


def _pick(seq, seed):
    return seq[seed % len(seq)]


def entity_name(prefix: str, seed: int) -> str:
    root = _pick(_ROOTS, seed)
    nature = _pick(_NATURES, seed // 3 + 1)
    base = f"{root} {nature}"
    if prefix == "LLC":
        return f"{base} {_pick(_LLC_SUFFIX, seed)}"
    if prefix == "LP":
        return f"{base} {_pick(_LP_SUFFIX, seed)}"
    if prefix == "LLP":
        return f"{base} {_pick(_LLP_SUFFIX, seed)}"
    if prefix == "NP":
        return f"{base} {_pick(_NP_SUFFIX, seed)}"
    return f"{base} {_pick(_CORP_SUFFIX, seed)}"


def person(seed: int) -> str:
    return f"{_pick(_FIRST, seed)} {_pick(_LAST, seed // 2 + 1)}"


def agent(seed: int) -> str:
    return _pick(_AGENTS, seed)


def cra_number(seed: int) -> str:
    return f"P{_CRA_BASE + (seed % 5000)}"


def address(seed: int) -> dict:
    street = _pick(_STREETS, seed)
    town, zip_ = _pick(_TOWNS, seed // 2 + 1)
    return {"line1": street, "city": town, "state": "ME", "zip": zip_}


def long_purpose(seed: int) -> str:
    """A deliberately long string to force overflow into a schedule."""
    nature = _pick(_NATURES, seed)
    return (
        f"To engage in the business of {nature.lower()} and any and all lawful "
        "activities related thereto, including without limitation the purchase, "
        "lease, manufacture, distribution, marketing, and sale of goods and "
        "services throughout the State of Maine and elsewhere; to acquire, hold, "
        "and dispose of real and personal property; to borrow money and issue "
        "obligations; and to do everything necessary, proper, or incidental to "
        "the accomplishment of the foregoing purposes, to the fullest extent "
        "permitted by the laws of the State of Maine."
    )
