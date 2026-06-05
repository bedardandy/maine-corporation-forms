# LP_MLPA-17 — Statement of Correction (Limited Partnership — Maine or Foreign)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 25  
**Mapped fields:** 23  
**Filer role:** at least one general partner of the LP per 31 MRSA §1324.1.J (individual GP signs on the upper block; alternative entity-GP signs via the lower 'For General Partner(s) which are Entities' block)

## Purpose

Correct false or erroneous information or a defectively-signed record previously filed with the Maine Secretary of State by a Maine domestic or foreign limited partnership under 31 MRSA §1327. Identifies the original record name and filing date, describes the error (FOURTH), provides the corrected text (FIFTH), and — for foreign LPs only — recites the home jurisdiction and Maine authorization date (SEVENTH). The correction is effective retroactively to the original filing date except for purposes of 31 MRSA §1303.3 and 4 (third-party reliance). Filing fee $50.

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
- Open question: THIRD ('Said record contained false or erroneous information or was defectively signed.') and SIXTH (retroactive-effect recital) are fixed statutory recitals with no widgets — they don't require filer input.
- Open question: SEVENTH is the foreign-LP-only block. Synth/rubric should branch on whether the form is being filed by a foreign LP; for domestic LPs both Text6 and Text7 should be left blank.
- Open question: Text11 column header reads '(type or print name)' rather than '(type or print name and capacity)' as on MLPA-12A/12B — but the field still serves as the entity-GP authorized-signer slot per the per-officer-signer convention. Treat as a minor template-label inconsistency, not a different canonical primitive.
- Open question: Footnote * permits 'any duly authorized person' alongside GPs in some interpretations of §1324.1.J; the rubric strictly enforces GP signature here per the form's own 'General Partner(s)' headers.
