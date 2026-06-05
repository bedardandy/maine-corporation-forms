# Templating, e-signature & document-assembly export

`tools/export/` turns a form's `mapping.json` + `schema.json` (+ `rubric.yaml`
for required flags, `form.yaml` for title/URL) into ready-to-import artifacts for
common third-party systems. It is **additive and deterministic** — it reads the
shipped per-form contract and writes import files; it never modifies a form or a
PDF.

```bash
# one form, one target, to stdout
python3 tools/export/export_form.py --form CORP_MBCA-6 --target esign

# every form, every target, to a build dir
python3 tools/export/export_form.py --all --target all --out build/
```

Artifacts land under `<out>/<form_id>/<target>/`.

## The neutral model

`export/model.py:build_model()` normalizes a form into a `FormModel` — a flat
list of `ExportField` with a small, stable vocabulary, so each exporter is a
type table, not bespoke logic. Each field carries both handles:

- **`field_id`** — the canonical dotted key (`clerk.cra_public_number`). This is
  the **data contract**: what an integrator binds their matter data to.
- **`acroform_names`** — the real PDF field name(s) (`Text3`, `Check Box15`).
  This is the **import handle**: what exists in the official AcroForm.

These forms are AcroForm-native, so the two differ — and which one an artifact
keys on depends on the target (below). The runtime field-split renames a shared
widget to `<T>__p<page>` *at fill time only*; the official PDF keeps the base
name, so the model de-promotes (`Check Box15__p4` → `Check Box15`) for any
artifact that imports into the official PDF.

`data_type` is one of `string | integer | number | boolean | date | enum`;
`binding` is `data | enum | boolean | signature`. `when` (from the planner's
harvested conditions) and `required` (from `severity: required` rubric checks)
ride along so conditional logic survives the export.

## Targets

| Target | Files | Keys on | For |
|--------|-------|---------|-----|
| `interchange` | `template.xfdf`, `data_dictionary.csv`, `case_schema.json` | XFDF: **AcroForm name**; schema/dict: **field_id** | Generic AcroForm fill (Adobe/iText/pdftk) + a typed case schema |
| `esign` | `docusign_template.json`, `pandadoc_fields.json` | **AcroForm name** (anchor/label) | DocuSign / PandaDoc tab placement |
| `docassembly` | `variables.json`, `merge_tokens.csv`, `logic.md` | **field_id** | Clio Draft / MyCase / HotDocs / Gavel merge tokens + branching |
| `gavel` | `gavel_variables.json` | **field_id** | Gavel (formerly Documate) variable set |

- **`template.xfdf`** is keyed by the real AcroForm field name so it imports
  straight into the blank official PDF (fetch it from `form.yaml.source_url`).
- **`case_schema.json`** and **`data_dictionary.csv`** are keyed by `field_id`
  (the data contract); the dictionary also lists the AcroForm name(s) each key
  drives, plus `type`, `binding`, `required`, `enum`, `when`, `page`,
  `confidence`.
- **e-sign** anchors tabs on the AcroForm field name (DocuSign imports AcroForm
  fields directly); `pandadoc_fields.json` carries both the `merge_field`
  (`field_id`) and the `acroform_field`.
- **doc-assembly** emits per-vendor merge tokens (Clio `{{Matter.Custom.x}}`,
  MyCase `[[x]]`, HotDocs `«x»`, Gavel `{{x}}`) and a human-readable `logic.md`
  of the `when` conditions.

## Notes

- Requires `PyYAML` (already in `requirements.txt`).
- Output is a pure function of the per-form contract — re-running is idempotent
  and safe to commit or to `.gitignore` as a build product.
- Not legal advice. Exported templates produce drafts for review, not filed
  documents.
