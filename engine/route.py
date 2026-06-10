"""Deterministic lexical router over the form catalog.

Given a free-text intent, returns candidate ``form_id`` values ranked by a
simple token-overlap score against each form's title, code, and entity type.
No network, no embeddings.

The standard router — used by the skill, MCP server, and HTTP API — is
``tools/route_form.py``, whose lexical fallback subsumes this module. This
minimal scorer is kept as a zero-dependency offline fallback (and for the
Makefile ``route`` target); prefer ``route_form`` in new integrations.
"""
import json
import re
from pathlib import Path

_TOKEN = re.compile(r"[a-z0-9]+")


def _tokens(text):
    return set(_TOKEN.findall((text or "").lower()))


def load_index(catalog_root="catalog"):
    path = Path(catalog_root) / "forms_index.json"
    return json.loads(path.read_text(encoding="utf-8"))["forms"]


def route(intent, catalog_root="catalog", top_k=5):
    """Return up to ``top_k`` (form_id, score, title) candidates for ``intent``."""
    query = _tokens(intent)
    if not query:
        return []
    forms = load_index(catalog_root)
    scored = []
    for form in forms:
        haystack = _tokens(
            " ".join([
                form.get("title", ""),
                form.get("code", ""),
                form.get("entity_type", ""),
                form.get("form_id", ""),
            ])
        )
        overlap = query & haystack
        if not overlap:
            continue
        score = len(overlap) / len(query)
        scored.append((form["form_id"], round(score, 3), form.get("title", "")))
    scored.sort(key=lambda t: (-t[1], t[0]))
    return scored[:top_k]


def _cli(argv):
    if len(argv) < 2:
        print("usage: python -m engine.route \"<intent text>\" [catalog_root]")
        return 1
    intent = argv[1]
    catalog_root = argv[2] if len(argv) > 2 else "catalog"
    for form_id, score, title in route(intent, catalog_root):
        print(f"{score:5.3f}  {form_id}  {title}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(_cli(sys.argv))
