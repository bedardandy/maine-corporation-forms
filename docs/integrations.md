# Integrations

How a downstream application drives this library. The contract is the per-form
folder; the engine is an optional reference consumer of it.

## The four operations

### 1. Route — pick the form(s)

```python
from engine import route
candidates = route.route("form a new business corporation")
# -> [(form_id, score, title), ...]
```

`route.route` ranks `catalog/forms_index.json` by lexical overlap (title + code
+ entity type). No network, no embeddings. For entity-scoped browsing, read
`catalog/by_entity.json`.

### 2. Build the case data

Assemble the nested case-data object (see `data-model.md`). Reuse canonical keys
across forms so one entity profile fills many filings:

```python
case = {
  "entity": {"name": "Wabanaki Widgets, Inc.", "authorized_shares": "1000"},
  "clerk":  {"name": "Downeast Registered Agents, LLC",
             "cra_public_number": "P99999", "is_noncommercial": False},
  "filing": {"contact": {"name": "...", "email": "...", "phone": "..."}},
}
```

### 3. Validate (optional)

```python
from engine import schema
errors = schema.validate("CORP_MBCA-6", case)   # [] when valid
```

Lightweight type / enum / required checks against the form's `schema.json`. For
the *conditional* rules (required-when), read `forms/<ID>/rubric.yaml` — each
check lists `depends_on_keys` and a severity, ready to evaluate in your app.

### 4. Fill

```python
from engine import fill
out = fill.fill("CORP_MBCA-6", case, "out.pdf")
```

or from the command line:

```bash
python3 -m engine.fill CORP_MBCA-6 case.json out.pdf
```

The filler resolves each canonical key from the case data, writes text widgets,
and checks boxes (truthy → the widget's non-`/Off` on-state). A canonical key
that maps to several widgets writes the same value to all of them.

## Reading artifacts directly

You don't need the engine. Everything is plain JSON / CSV / YAML:

```python
import json, pathlib
form = pathlib.Path("forms/CORP_MBCA-6")
mapping = json.loads((form / "mapping.json").read_text())
schema_ = json.loads((form / "schema.json").read_text())
# mapping["map"] is keyed by the PDF AcroForm field (the direction shared
# with the sibling forms repos); each binding carries its canonical case key.
for field_id, binding in mapping["map"].items():
    print(field_id, "<-", binding["key"], binding["confidence"])
```

(`engine.mapping.entries(mapping)` presents the same data keyed by canonical
case key, with `widget_id` / `options` reconstructed, if your integration
prefers the case-side view.)

A docassemble interview, a LangChain tool, a PandaDoc sync, or a custom backend
can each consume `mapping.json` + `schema.json` directly and use its own PDF
writer.

## More layers

All optional and additive; the per-form contract + `engine/` stay the substrate.

- **Coverage & conditional gating** — `python3 -m engine.plan <ID> case.json`
  reports resolved / unresolved (required) / skipped (gated off by `when`). See
  `engine/README.md`.
- **Templating / e-sign / doc-assembly export** — `tools/export/` →
  XFDF, DocuSign, PandaDoc, Clio, MyCase, HotDocs, Gavel. See
  [templating.md](templating.md).
- **Router, HTTP API & MCP agent** — `tools/route_form.py`,
  `tools/api_server.py`, `tools/agent_server.py` + `.codex-plugin/`. See
  [router-and-api.md](router-and-api.md).
- **Accessibility** — `tools/accessibility/remediate_form.py` sets field
  tooltips, title, and language deterministically (see its README).
- **Fuzz harness** — `python3 tools/fuzz.py` exercises every form against
  hostile case shapes (0 findings expected).

## Trust and verification

Surface per-field `confidence` to the user and treat low/medium as unverified.
Always state the output is a draft to be checked against the official form before
filing. See `PROVENANCE.md` and `docs/STATUS.md`.
