# CORP_MBCA-12B — Application of Withdrawal (Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 23  
**Mapped fields:** 20  
**Filer role:** duly authorized officer of the foreign corporation per 13-C MRSA §121.5 (signs at bottom of page 0)

## Purpose

Withdraw a foreign business corporation's authority to transact business in Maine under 13-C MRSA §1521 or §1523. The form recites the foreign corporation's home jurisdiction, the date Maine authority was granted, an optional FOURTH block for withdrawal upon conversion to a nonfiling entity (entity type + governing jurisdiction), and a FIFTH block providing a mailing address for service of process during the withdrawal period. Signed by a duly authorized officer.

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

- `withdrawal.conversion.new_entity_type` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: FOURTH wraps onto two lines: 12b4 is the inline trailing blank for 'converted is ____' on line 1; 12b5 is a narrow (~63pt) leading blank on line 2 that receives any overflow of the new-entity-type value; 12b6 is the wider trailing blank on line 2 for 'internal affairs is ____' (governing jurisdiction). Drafter originally collapsed 12b6/12b7 into withdrawal.service_of_process_mailing_address — fixed in this review. 12b7 is the standalone full-width FIFTH address line.
- Open question: FOURTH has no opt-in checkbox — the filer fills both blanks (or leaves both empty) based on whether the withdrawal is upon conversion. Rubric enforces all-or-nothing rather than requiring an explicit boolean.
- Open question: The (signature of duly authorized officer) line above 12b9 is wet-ink only and has no AcroForm widget — consistent with other Shape-D forms. Only the printed-name-and-capacity widget (12b9) is bound.
