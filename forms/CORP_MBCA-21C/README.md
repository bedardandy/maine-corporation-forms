# CORP_MBCA-21C — Statement of Abandonment of Entity Conversion

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 18  
**Mapped fields:** 16  
**Filer role:** officer or other duly authorized representative of the corporation (per the page-0 footnote and 13-C MRSA §958.2)

## Purpose

Abandon a previously filed Articles of Entity Conversion (Form MBCA-21) OR Articles of Charter Surrender (Form MBCA-20A) before the conversion becomes effective, pursuant to 13-C MRSA §958. Filed by a domestic business corporation to halt a pending entity conversion. The form (2 pages, 18 widgets) captures the entity name, the date the original conversion was scheduled to become effective (FIRST), the filing date (DATED), the signer's name and capacity (Shape D), plus the standard cover-letter primitive on page 2. Filing fee is $35 per the page-0 header. Direct sibling of MBCA-20B (which abandons the nonprofit-conversion form MBCA-20).

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
- Open question: FIRST captures the future effective date of either the prior MBCA-21 (Articles of Entity Conversion) or the prior MBCA-20A (Articles of Charter Surrender). The form does not distinguish which prior filing is being abandoned — per §958.2, the SOS identifies the prior filing by entity name + filing date. Mapped to existing conversion.future_effective_date per MBCA-20B precedent.
- Open question: SECOND (immediate-effect recital) has no widget — it is a representation by the corporation, not a captured field.
- Open question: Form has no widget for the actual signature line — only the typed-name-and-capacity widget. Wet-ink only (same convention as MBCA-13A, MBCA-20B and other Shape-D forms).
- Open question: Field-id naming is mixed-case ('21cOne', '21cTwo', '21cThree', '21cFour') — preserved verbatim, parallel to MBCA-20B's '20bOne'/'20BTwo' style. Filler engine must handle both.
- Open question: Drafter initially proposed conversion.scheduled_effective_date as a new schema-gap key; corrected to conversion.future_effective_date during review per MBCA-20B precedent (semantically the same date, just referenced from the abandonment perspective).
