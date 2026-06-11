# LLC_MLLC-5A — Termination of Statement of Intention to Transact Business Under an Assumed or Fictitious Name (Maine or Foreign LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 19  
**Mapped fields:** 19  
**Filer role:** a person authorized by the LLC (per page-0 footnote: '*Pursuant to 31 MRSA §1676.1B, this statement MUST be signed by a person authorized by the limited liability company')

## Purpose

Terminate a previously filed Statement of Intention to Transact Business Under an Assumed or Fictitious Name for a Maine or Foreign LLC under 31 MRSA §1510.7 (and §1676.1B for the signature requirement). Captures the LLC's legal name, the assumed/fictitious name being terminated, and up to two parallel 'Authorized Person' signer blocks.

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
- Open question: Form is for 'Maine or Foreign LLC' — entity.name is the Maine-record name (used here per termination-of-Maine-registration semantics), but for foreign LLCs the home-jurisdiction name (entity.home_jurisdiction_name) may also need to be referenced. Confirm whether the form expects only the Maine-record name or whether a foreign LLC must disclose both.
- Open question: Form has TWO inline 'Authorized Person(s)*' signer slots (Text4, Text5) but no entity-signer block (unlike MLLP-5A which has both individual and entity slots). Reviewer mapped to filing.signer_N.* (multi-slot extension of filing.signer.*) rather than partner_N.* (role-specific) since LLC's 'authorized person' role is generic and doesn't fit the role-keyed multi-slot patterns used for LLP/LP forms.
- Open question: Page-0 footnote cites 31 MRSA §1676.1B for signature authority. Confirm that no separate disclosure of the original Statement-of-Intention filing date is required by §1510.7.
- Open question: Sibling form: LLP_MLLP-5A (LLP termination) is structurally analogous but uses single-slot filing.signer.* + filing.signer_entity.* (only one widget per signer type). LLC's MLLC-5A has two parallel individual slots and no entity slot — different signer-block shape, different canonical-key family despite the same form purpose.
