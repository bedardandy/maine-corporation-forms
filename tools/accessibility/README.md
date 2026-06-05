# Accessibility remediation

`remediate_form.py` makes a form PDF more accessible using only what the
per-form contract already provides — deterministically, no model, no guessing.

```bash
# remediate a blank form by id (title comes from form.yaml)
python3 tools/accessibility/remediate_form.py CORP_MBCA-6 --out out.pdf

# remediate any filled PDF, pointing at the form's mapping for labels
python3 tools/accessibility/remediate_form.py filled.pdf \
    --mapping forms/CORP_MBCA-6/mapping.json \
    --title "Articles of Incorporation" --out out.pdf
```

## What it sets

| Item | Source | WCAG / PDF-UA |
|------|--------|---------------|
| Field tooltip `/TU` on every widget | the field's `label` in `mapping.json` | 1.3.1 / 4.1.2 (a screen reader speaks each field) |
| Document `/Title` + `DisplayDocTitle` | `form.yaml` title | 2.4.2 (viewer shows the form name) |
| `/Lang` | `--lang` (default `en-US`) | 3.1.1 |

List `widget_id`s and runtime-split shared checkboxes (`Check Box15__p4`) all
resolve to their field's label, so every underlying widget gets a tooltip.

## What it does not do

It does **not** build a structure tree (tags / `StructTreeRoot`) and it never
sets `/MarkInfo /Marked true`. A correct content tag tree (PDF/UA 7.1/7.2 —
reading order, headings, tables) needs layout understanding this tool doesn't
have, and a faked `/Marked` flag fails PDF/UA worse than honest absence. That
step needs Adobe Acrobat / an auto-tagger; the tool prints a note saying so.
