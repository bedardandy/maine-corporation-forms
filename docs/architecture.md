# Architecture

## The form folder is the unit

Everything is organized around a self-contained `forms/<FORM_ID>/` folder. No
tool needs to reach outside the folder to fill a form (except the optional
shared `engine/`). This is what makes the library portable and lets forms be
added, reviewed, and shipped one at a time.

## Data flow

```
blank SoS PDF ──► AcroForm field list ─┐
                                       ├─► mapping.json  (canonical_key -> widget)
pass-1 field analysis ─────────────────┘   schema.json   (JSON Schema for fill data)
   (purpose, keys, types, rubric)          fields.csv    (flat inventory)
                                           rubric.yaml   (conditional rules)
                                           form.yaml / README.md / SKILL.md
                                                 │
                       case-data object ──► [engine.fill] ──► filled PDF
                                                 │
                                          [engine.schema] ──► validation errors
```

The generator (`tools/build_from_pass1.py`) is the only thing that writes the
per-form artifacts. The engine only *reads* them.

## The per-form contract

| File | Role |
|------|------|
| `<ID>.pdf` | the blank Maine SoS form (public record) |
| `form.yaml` | metadata: code, title, entity type, statute, page/field counts |
| `mapping.json` | `map: {field_id -> {key, field_type, page, confidence, label, ...}}` (PDF-field-keyed, the direction shared with the sibling repos; `engine/mapping.py` documents the dialect) |
| `schema.json` | draft-2020-12 JSON Schema for the case-data object |
| `fields.csv` | flat field inventory (widget, page, type, label, key, confidence) |
| `rubric.yaml` | validation checks with `depends_on_keys` + severity |
| `README.md` | purpose, statute, filer role, known ambiguities |
| `SKILL.md` | agent fill-guide: when to use, key fields, conditional logic, example |

A binding may carry a `widgets` **list** when one canonical key drives several
widgets (e.g. a clerk name that appears on both the commercial and
noncommercial rows); the binding anchors on the first widget and the engine
writes the same value to all of them.

## The canonical model

Fill data is a single nested object keyed by dotted canonical keys
(`entity.name`, `clerk.cra_public_number`, `filing.contact.email`,
`filing.entities[0].name`). The same keys are reused across every form so a
downstream app builds one entity profile and fills many forms from it. The model
is documented in `data-model.md`; the naming taxonomy in `field-schema.md`.

## Deterministic engine

`engine/` writes PDFs through the shared `maine-forms-engine` fill core
(PyMuPDF) with this repo's policy layered on top (pypdf remains only for the
shared-field runtime split and offline tooling). No network, no LLM at fill
time:

- `canonical.py` — resolve a dotted key (with list indexing) against the case data.
- `schema.py` — lightweight type/enum/required validation against `schema.json`.
- `fill.py` — load `mapping.json` + the PDF, resolve each key, write text values
  and check boxes (truthy → the widget's non-`/Off` on-state), save the PDF.
- `route.py` — rank candidate forms for a free-text intent by lexical overlap
  over `catalog/forms_index.json`. No embeddings.

## Validation

`schema.json` enforces structure (types, enums, minimal required keys).
`rubric.yaml` captures the *conditional* business rules that a flat schema can't
— e.g. "if `clerk.type` = commercial, `clerk.cra_public_number` is required",
"exactly one share structure", "director min ≤ max". The engine ships schema
validation; rubric evaluation is left to the integrator (the rules are
machine-readable).
