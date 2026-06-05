# CORP_MBCA-6A — Restated Articles of Incorporation

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 26  
**Mapped fields:** 21  
**Filer role:** duly authorized officer or the clerk of the corporation (per 13-C MRSA §121.5)

## Purpose

File Restated Articles of Incorporation for a Maine domestic business corporation under 13-C MRSA §1007. The restatement consolidates all prior amendments into a single document, optionally adding a new amendment. The full restated text MUST be attached as an exhibit (typically the contents of MBCA-6-1).

## Field mapping

This directory contains a machine-readable mapping between canonical data keys and the PDF's AcroForm widget names.

| File | Purpose |
|------|---------|
| `form.yaml` | Form metadata |
| `mapping.json` | canonical_key to widget mapping |
| `schema.json` | JSON Schema for fill data |
| `fields.csv` | Flat field inventory |
| `rubric.yaml` | Validation checks |
| `README.md` | This file |
| `SKILL.md` | Agent fill guidance |

## Known ambiguities

- `restatement.type` maps to 2 widgets; all receive the same value.
- `amendment.approval_method` maps to 3 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Per the form footnote, Form MBCA-6-1 (the body-text exhibit) MUST accompany this filing. Synth/assemble must bundle MBCA-6A with MBCA-6-1 and use the same restatement.text_exhibit_letter on both. Should `filing.bundled_forms[]` be added to track these dependencies?
- Open question: THIRD says 'set forth in Exhibit ___ or as follows:' but only the exhibit-letter widget (Text7) is bound — no inline-text widget. MBCA-9 has both `amendment.share_exchange_exhibit_letter` AND `amendment.share_exchange_inline_text` for the same conditional, but MBCA-6A omits the inline-text widget. This is likely an upstream template difference rather than a schema gap.
- Open question: FOURTH effective date applies to the restatement as a whole, not to the embedded new amendment. If a restatement bundles a new amendment AND specifies a future-effective date, both the restatement and the embedded amendment take effect on that date — confirm with §1007 that there is no separate amendment-effective-date concept here.
- Open question: No widget binds the actual signature line — only the printed-name-and-capacity (Text5). Wet-ink signature is implicit. Consistent with most other Maine SOS forms.
