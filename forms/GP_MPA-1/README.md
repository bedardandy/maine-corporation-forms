# GP_MPA-1 — Statement of Dissociation (General Partnership)

**Entity type:** General Partnership  
**Statute:** Maine Uniform Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** any partner of the partnership (individual or entity); see 31 MRSA §1005.3

## Purpose

File a Statement of Dissociation under 31 MRSA §1074 recording that a named partner has dissociated from a general partnership. The statement is signed by a partner (individual or entity); signature authority is governed by 31 MRSA §1005.3.

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
- Open question: Individual block (Text4) and entity block (Text5/Text6) are alternatives — the form layout makes them mutually exclusive but does not enforce it via a radio/checkbox. Captured as an exactly-one rubric check above.
- Open question: The (signature) and (authorized signature) lines have no AcroForm widgets — wet-ink signatures expected at fill time. Text4/Text6 capture the printed-name side only.
- Open question: Field-id 'cover' (no number) for the immediate-tier checkbox is a template anomaly. Filler should bind by exact field-id including the missing-suffix case.
