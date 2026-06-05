#!/usr/bin/env python3
"""Route a free-text situation to candidate Maine SoS business-entity forms.

A single LLM call over a compact, cached *router catalog* (form titles + a few
factual disambiguation hints). At ~156 forms the whole catalog is a few thousand
tokens and fits in one prompt, so no embeddings are needed. Falls back to a
lexical scorer when no LLM endpoint is reachable, so it always returns something.

Pluggable via env:
  ROUTER_BASE_URL   OpenAI-compatible base url (default http://localhost:8088/v1)
  ROUTER_MODEL      model name (default 'local')
  ROUTER_API_KEY    api key (default 'none')
  ROUTER_TOP_K      candidates to return (default 5)

    python3 tools/route_form.py "form a new business corporation in Maine"
    python3 tools/route_form.py "change our LLC's registered agent" --json
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "router_catalog.json"


def _load_catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["forms"]


def _lexical(query, forms, top_k):
    q = set(re.findall(r"[a-z0-9]+", query.lower()))
    if not q:
        return []
    scored = []
    for f in forms:
        hay = set(re.findall(
            r"[a-z0-9]+",
            (f["title"] + " " + " ".join(f.get("hints", []))
             + " " + f["form_id"]).lower()))
        overlap = len(q & hay)
        if overlap:
            scored.append((overlap, f["form_id"], f))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [f for _, _, f in scored[:top_k]]


def _llm(query, forms, top_k):
    base = os.environ.get("ROUTER_BASE_URL", "http://localhost:8088/v1")
    model = os.environ.get("ROUTER_MODEL", "local")
    key = os.environ.get("ROUTER_API_KEY", "none")
    catalog_lines = [
        f'{f["form_id"]}: {f["title"]}'
        + (f' [{"; ".join(f["hints"])}]' if f.get("hints") else "")
        for f in forms
    ]
    prompt = (
        "You are a form router for Maine Secretary of State business-entity "
        "filings. Given a user's situation, pick the most likely form id(s) "
        "from the catalog. Return ONLY a JSON array of form_id strings, best "
        f"first, max {top_k}. If none fit, return [].\n\n/no_think\n\n"
        "CATALOG:\n" + "\n".join(catalog_lines)
        + f"\n\nSITUATION: {query}\n\nJSON:"
    )
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 120,
    }).encode()
    req = urllib.request.Request(
        f"{base}/chat/completions", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    text = data["choices"][0]["message"]["content"]
    ids = json.loads(text[text.index("["):text.rindex("]") + 1])
    valid = {f["form_id"] for f in forms}
    return [i for i in ids if i in valid][:top_k]


def route(query, top_k=5):
    """Return ``(results, mode)`` — results is a list of catalog entries."""
    forms = _load_catalog()
    by_id = {f["form_id"]: f for f in forms}
    try:
        ids = _llm(query, forms, top_k)
        if ids:
            return [by_id[i] for i in ids], "llm"
    except Exception:
        pass
    return _lexical(query, forms, top_k), "lexical"


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("situation", help="free-text description")
    ap.add_argument("--top-k", type=int,
                    default=int(os.environ.get("ROUTER_TOP_K", "5")))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    results, mode = route(a.situation, a.top_k)
    if a.json:
        print(json.dumps({"mode": mode, "results": results}, indent=2))
    else:
        print(f"[{mode}]")
        for f in results:
            hint = f' [{"; ".join(f["hints"])}]' if f.get("hints") else ""
            print(f'  {f["form_id"]}: {f["title"]}{hint}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
