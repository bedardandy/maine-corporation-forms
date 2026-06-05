# CORP_MBCA-11 — Articles of Dissolution

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** any duly authorized officer OR the clerk (per 13-C MRSA §121.5)

## Purpose

Dissolve a Maine domestic business corporation under 13-C MRSA §1404, recording the original-filing date, dissolution-authorization date, optional future effective date, and (when applicable) shareholder approval.

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

- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: FOURTH has only one checkbox ('approved by shareholders') — for corporations that haven't issued shares, dissolution is authorized differently (by incorporators or directors). Does the form rely on leaving the checkbox unchecked in that case, or is there a missing path?
- Open question: Is the 'signature of any duly authorized officer' a separate signature widget that pypdf didn't extract, or expected to be added as an image/wet-ink overlay?
