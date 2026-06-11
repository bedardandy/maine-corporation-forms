# LLC_MLLCACSOA — Amendment or Cancellation of Statement of Authority (Maine LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 32  
**Mapped fields:** 31  
**Filer role:** an authorized person of the LLC (page-1 footnote text accompanies the two '(type or print name and capacity)' signature widgets — the form's body does not constrain the role beyond 'authorized person', mirroring the MLLC-5A authorized-person pattern)

## Purpose

Amend or cancel a previously filed Statement of Authority for a Maine LLC under 31 MRSA §1542.2. Captures the LLC's name, the original Statement-of-Authority filing date, a SECOND-recital radio that selects either an amendment or a cancellation, the affected person/position, up to 4 description lines for the chosen action, an optional additional-information exhibit letter, and up to 2 authorized-person signer blocks.

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
- Open question: The two SECOND-recital checkboxes (Check Box3 amendment, Check Box9 cancellation) are mapped to a single filing.action_type enum — same convention as the GP_CONV-PARTNER 4-way new-entity-type radio. Synth fills exactly one; filler engine writes the other as unchecked.
- Open question: The form's amendment-block (Check Box3 + person affected + 4 description lines) and cancellation-block (Check Box9 + affected + 4 description lines) are physically separate inline widgets — synth must populate exactly one block based on filing.action_type and leave the other empty (rubric enforces XOR via amendment-block-required-when-amendment / cancellation-block-required-when-cancellation).
- Open question: Two inline signer slots (name and capacity1, name and capacity2) match the MLLC-5A pattern. Form footnote text is not extracted — assume same '*Statement MUST be signed by a person authorized by the LLC' constraint as MLLC-5A.
- Open question: Field-id naming is bare-token style ('name', 'file date', 'amend1'..'amend4', 'cancel1'..'cancel4', 'dated', 'exhibit', 'name and capacity1'/2) rather than 'TextN'/'Check BoxN' — same template style as the older 'one1'..'one6' templates (MLLP-1) and 'cover1'..'cover14' templates (MLPA-6, GP_CONV-PARTNER). Filler engine should accept all naming styles.
