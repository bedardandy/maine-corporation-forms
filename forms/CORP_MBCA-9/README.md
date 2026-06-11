# CORP_MBCA-9 — Articles of Amendment

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 25  
**Mapped fields:** 25  
**Filer role:** duly authorized officer of the corporation (signs at bottom)

## Purpose

Amend the articles of incorporation of an existing Maine domestic business corporation under 13-C MRSA §§1006, 1004, 1005, 1011, including approval method, optional benefit-corporation status changes, share-exchange provisions, and effective date.

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

- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: The page-null 'duly' and 'bc' checkboxes are inferred to back the FIRST and SECOND radio groups, but pdftk dump_data_fields would confirm whether each is a single radio or a checkbox set with shared name.
- Open question: FIRST has a 3-option radio (incorporators / directors / shareholders) but only one logical 'duly' field; how does the PDF encode the 3 mutually-exclusive options? May need export-value lookup.
