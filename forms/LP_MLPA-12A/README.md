# LP_MLPA-12A — Application for Amended Certificate of Authority to Transact Business (Foreign Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 62  
**Mapped fields:** 62  
**Filer role:** at least one general partner of the foreign LP (individual or authorized representative of an entity GP) — §1324.1.M only requires one signer (cf. §1321 formation requirement of all GPs)

## Purpose

Amend the Certificate of Authority of a foreign limited partnership already authorized to transact business in Maine under 31 MRSA §1324. Captures changes to the entity's home-jurisdiction name (or adoption of a fictitious Maine name), additions/dissociations to the GP roster, address and name changes for current GPs, and updates to principal-office and required-office addresses.

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
- Open question: Two-tier fee structure ($90 full / $35 partial) is determined by which sections are populated — there's no explicit checkbox. Confirm SOS practice: presumably $35 applies when only Items SIXTH–NINTH are populated and $90 when any of SECOND–FIFTH (or any combination) is populated.
- Open question: Page 0 widget naming skips Text8–13 (jumps Text7→Text14) and page 2 skips Text54. These are template artifacts, not missing widgets — preserved verbatim.
- Open question: Page 2 has only one inline individual-signer slot (vs. 3 on LP_MLPA-6 formation). §1324.1.M requires only one GP signature, so this is intentional.
- Open question: Should `entity.required_office.*` carry an applicability flag (boolean for whether home-jurisdiction laws require the office)? The form says 'If no change, so indicate' which implies the section can be left blank — the absence of a value already encodes 'not applicable'.
