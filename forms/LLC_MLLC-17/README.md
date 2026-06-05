# LLC_MLLC-17 — Statement of Correction (Limited Liability Company — Maine or Foreign)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 22  
**Mapped fields:** 20  
**Filer role:** a person authorized by the limited liability company per 31 MRSA §1676.1B (signs at bottom of page 1; up to two authorized persons may sign — the second slot is optional)

## Purpose

Correct an incorrect or inaccurate record previously filed with the Maine Secretary of State by a Maine or foreign LLC under 31 MRSA §1675. Identifies the original filing date and document name, describes the error and the corrected information, and is signed by up to two authorized persons (per 31 MRSA §1676.1B). Filing fee $50. The correction is effective retroactively to the original filing's effective date except as to third parties that previously relied on the uncorrected record (FIFTH).

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
- Open question: The form provides two '*Authorized person' signature blocks on page 1. The form text doesn't explicitly say the second is optional, but 31 MRSA §1676.1B requires only one authorized signer. The rubric treats signer_2 as optional. Confirm whether SOS rejects single-signed corrections in practice.
- Open question: The form serves both Maine domestic and foreign LLCs from a single body 'entity.name' widget (no entity.home_jurisdiction_name slot). For foreign-LLC corrections, synth should populate entity.name with the foreign LLC's home-jurisdiction legal name (which is also what's on file with Maine SOS). This deviates from the entity-name-vs-home-jurisdiction.md convention which is grounded in forms that distinguish them — MLLC-17 does not.
- Open question: FIFTH paragraph (retroactive-effect recital) has no widgets — it is a fixed statutory recital that doesn't require filer input.
