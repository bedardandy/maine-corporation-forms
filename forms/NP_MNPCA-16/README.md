# NP_MNPCA-16 — Approval of Local Development Corporation by Municipal Officers

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 1  
**Fields:** 11  
**Mapped fields:** 11  
**Filer role:** Municipal Clerk attesting to the council/select-board vote (signs and affixes the municipal seal); the underlying voters are the municipality's officers themselves

## Purpose

Record the majority vote of municipal officers authorizing the formation of a Local Development Corporation (LDC) under 5 MRSA §13120-B.9. Filed as an attachment to the Articles of Incorporation (NP_MNPCA-6) for an LDC; carries no cover letter of its own and 'No Fee Required' (the LDC's MNPCA-6 carries the standard $40 fee).

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

- Open question: This form has no cover-letter primitive widgets — it is a one-page attachment to NP_MNPCA-6 and inherits the MNPCA-6 cover letter. The synth builder must compose the bundle (MNPCA-6 + this form) as a single submission packet; rubric should treat the cover letter as an MNPCA-6 concern, not an MNPCA-16 concern.
- Open question: 5 MRSA §13120-B.9 does not specify a minimum number of signing officers; the form's instruction is 'majority vote' which is a statutory standard rather than a syntactic one. The rubric majority-officers-signed check is therefore a soft floor (≥1 row populated); a true majority check requires knowledge of the municipality's governing body composition (e.g., a 7-member council needs ≥4 signatures).
- Open question: Five physical signature lines exist on the form (right-hand column, mirroring the 5 name-and-capacity blanks) but none have AcroForm widgets — wet-ink overlay only. Same convention as Shape-D forms; not a missing-widgets bug.
- Open question: (Affix Municipal Seal) is a wet-ink instruction with no widget — assumed to be a physical stamp added after PDF generation.
