# LLC_MLLCDENIAL — Statement of Denial of Authority (Maine LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 18  
**Mapped fields:** 18  
**Filer role:** the person whose authority is being denied — either named individually in the original Statement of Authority or holding a position named there (signs at bottom of page 0 over '(type or print name and capacity)')

## Purpose

File a Statement of Denial of Authority for a Maine limited liability company under 31 MRSA §1543. The signer denies the authority that a previously filed Statement of Authority granted them — either by name (as an authorized person) or by virtue of holding a position the prior statement named. Under §1543, the denial operates as a limitation cancelling the granted authority. Per §1676.1.D, the denial must be signed by the person who is denying. The signer must furnish a copy of the denial to the LLC.

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
- Open question: Form recital states 'I further state that I have furnished the limited liability company with a copy of this statement of denial as required under 31 MRSA §1543.3' — this is an attestation, not a separate fillable widget. No additional canonical key needed; signing the form is the attestation. Reviewer should not invent a 'denial.copy_furnished' boolean.
- Open question: The capacity in filing.signer.printed_name_and_capacity is constrained by the original Statement of Authority: the signer is denying authority that ran either to them by name or to a position they hold. The capacity should typically read 'Authorized Person' (matching the §1542 / §1543 vocabulary) or the title of the position the original Statement named. Synth must coordinate this value with the (hypothetical) original Statement; for synthetic data the capacity value is free-form.
- Open question: Cover-letter Immediate-expedite checkbox is named 'Check Box16' here (other LLC forms in this corpus use bare 'cover' for this widget). Note the per-form template variation; synth must use the field_id from this form's widgets.json, not assume.
