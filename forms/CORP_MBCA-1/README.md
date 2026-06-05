# CORP_MBCA-1 — Application for Reservation of Name

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 19  
**Mapped fields:** 17  
**Filer role:** applicant (any person reserving a name on behalf of an intended business corporation)

## Purpose

Reserve a corporate name for 120 days under 13-C MRSA §402.1 prior to incorporating; reservation cannot be renewed.

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
- Open question: Is the 'signature of applicant' a separate signature widget that pypdf didn't extract, or is it expected to be filled outside the AcroForm (wet-ink/image overlay)?
- Open question: On a name-reservation filing, the cover-letter 'annual report reminders email' field is meaningless (no entity is created). Should we still encourage filling it, or leave it blank? Possibly clarify with SOS.
