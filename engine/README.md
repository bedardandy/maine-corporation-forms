# Reference fill engine

A dependency-light (standard library + `pypdf`) reference consumer of the
per-form folders. It is **optional** — the per-form `forms/<ID>/` contract is
the portable substrate; this engine is how the project fills and verifies a
form. No network and no LLM at fill time: filling is fully deterministic.

## Modules

| File | Role |
|------|------|
| `canonical.py` | resolve a dotted canonical key (with list indexing, `items[0].name`) against a nested case-data dict |
| `mapping.py` | the canonical-direction `mapping.json` dialect (PDF-field-keyed `map`, shared with the sibling repos): loader, `entries()` consumer view, lossless direction converter core |
| `schema.py` | lightweight validation of case data against a form's `schema.json` (types, enums, required) |
| `fill.py` | load `mapping.json` + the blank PDF, resolve each key, write AcroForm values, save the filled PDF |
| `plan.py` | report coverage for a case *without* a PDF — resolved / unresolved (missing facts) / skipped (gated off by `when`) |
| `route.py` | rank candidate forms for a free-text intent over `catalog/forms_index.json` (lexical, no embeddings) |

## Fill a form

```bash
pip install -r ../requirements.txt        # pypdf, PyYAML
python3 -m engine.fill CORP_MBCA-6 examples/corp_mbca-6.case.json out.pdf
```

This resolves `forms/CORP_MBCA-6/mapping.json` and
`forms/CORP_MBCA-6/CORP_MBCA-6.pdf`, fills each mapped widget, and writes
`out.pdf`. Pass an optional 4th arg to point at a different `forms/` root.

## Plan coverage (no PDF)

```bash
python3 -m engine.plan CORP_MBCA-6 examples/corp_mbca-6.case.json
```

Reports which canonical keys are **resolved**, **unresolved** (missing facts;
`required: true` when a `severity: required` rubric check depends on the key),
and **skipped** — gated off because the field's `when` condition is definitively
false for this case. Add `--full` for the JSON plan.

### Conditional gating (`when`)

A `mapping.json` field may carry a `when` expression; the field is *not
applicable* to a case when that expression is false. Grammar: `LHS == v`,
`LHS != v`, `LHS == true|false`, `LHS in ['a','b']`, or bare `LHS` (truthy),
where `LHS` is a dotted canonical key. Gating is **conservative**: a field is
skipped only when its controller is *known* and the condition is false; an
unknown controller leaves the field surfaced (the safe default for legal forms).

These conditions are harvested from `rubric.yaml` prose by
`tools/harvest_when.py` (idempotent; only the cleanly-parseable, schema-verified
subset — `"If X is true, …"` / `"If X = 'v', …"` whose value is a real enum
member). Re-run it after editing a rubric:

```bash
python3 tools/harvest_when.py            # write `when` onto mappings
python3 tools/harvest_when.py --dry-run  # report only
```

## Route an intent

```bash
python3 -m engine.route "form a new business corporation"
```

(`engine.route` is the minimal offline lexical scorer; the standard
router used by the skill, MCP server, and HTTP API is
`tools/route_form.py`, which subsumes it.)

## Programmatic use

```python
from engine import canonical, schema, fill, plan, route

errors = schema.validate("CORP_MBCA-6", case_data)   # [] when valid
fill.fill("CORP_MBCA-6", case_data, "out.pdf")
canonical.get(case_data, "filing.entities[0].name")
route.route("change of registered agent")
```

## `mapping.json` direction

`mapping.json` is keyed by the **PDF AcroForm field** (`map: {field_id:
{key, ...}}`), the direction shared with the sibling forms repos; see
`engine/mapping.py` for the dialect (multi-widget fan-outs anchor on their
first widget and keep the ordered list under `widgets`; `enum_select` /
`enum_text_select` groups anchor on their first option widget). Engine and
tooling consume bindings through `engine.mapping.entries(mapping)`, the
case-key-keyed view with `widget_id` / `options` reconstructed — every
description of "entries" below refers to that view.
`tools/convert_mapping_direction.py` converts (and `--check`s) the files.

## Field types in `mapping.json`

Each entry's `field_type` is one of:

- `text` (default) — the stringified value is written to the widget.
- `checkbox` / `boolean` — see below.
- `radio` — a mutually-exclusive `/Btn` group; see below.

## Checkbox handling

For a field typed `checkbox` (or `boolean`), a truthy value sets the widget to
its **on-state** — the appearance-dictionary key that is not `/Off` (commonly
`/Yes`). A falsy value leaves the box unchecked. Text fields receive the
stringified value.

The engine resolves the field by its parent `/T` name and sets the parent `/V`
plus the `/AS` of **every kid annotation** (falling back to the field's own
`/AS` when it has no kids). This renders checkboxes whose widget is split
across multiple kid annotations on different pages — a quirk of some SoS forms.
Note: when a single `/Btn` parent drives two boxes on **different pages** (a
shared-field collision in some SoS PDFs), the engine splits them first (see
"Shared multi-page checkbox repair" below) so each box is set independently.

## Radio handling

A field typed `radio` targets a `/Btn` group by its parent `/T` name
(`widget_id`). The resolved value is looked up in the entry's `options` map
(`{enum_value: on_state_export_name}`) to find the on-state export name; the
engine sets the parent `/V` and the matching kid widget's `/AS` to that
on-state and forces every sibling kid to `/Off`. Two distinct groups may
legitimately reuse the same export names (e.g. `bene`/`bene1`) as long as
their parent group names differ.

## Shared-widget keys

When a canonical key's `widget_id` is a **list**, the same resolved value is
written to every listed widget (e.g. a clerk name that appears on more than one
row of the form).

## Shared multi-page checkbox repair

Some SoS PDFs reuse one `/Btn` field name for two unrelated checkboxes on
different pages (e.g. a substantive certificate box and the cover-letter
"expedited filing" box) — toggling the field would check both. Before filling,
`split_shared_fields()` promotes each such kid widget into its own terminal
field named `<T>__p<page>` (0-based page index) **in the in-memory writer
only**; the source PDF on disk is never modified. Mappings for the affected
forms address the boxes by their promoted names (e.g. `Check Box15__p4`). Radio
groups are left untouched. Affected forms are listed in
`tools/HAND_MAINTAINED.txt`.

## Not included

This engine does not render, flatten, or visually audit the output, and it does
not auto-fit overflowing text. Those are integrator concerns. Validate the
output by opening the filled PDF (or reading field values back with `pypdf`).
