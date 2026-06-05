"""Canonical nested-dict resolver.

Resolves dotted canonical keys against a nested case-data dictionary, with
support for list indexing (``entities[0].name``).
"""


def get(data, dotted_key, default=None):
    """Resolve a dotted path like ``a.b.c`` or ``items[0].name`` from nested data.

    Returns ``default`` if any segment is missing or an index is out of range.
    """
    cur = data
    parts = dotted_key.replace("]", "").replace("[", ".").split(".")
    for part in parts:
        if part == "":
            continue
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return default
        elif isinstance(cur, dict):
            if part not in cur:
                return default
            cur = cur[part]
        else:
            return default
    return cur


def has(data, dotted_key):
    """Return True if the dotted key resolves to a non-None value."""
    sentinel = object()
    return get(data, dotted_key, sentinel) is not sentinel
