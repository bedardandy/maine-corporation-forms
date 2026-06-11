# NP_MNPCA-12B — Application for Surrender of Authority to Carry on Activities (Foreign Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 21  
**Mapped fields:** 21  
**Filer role:** duly authorized individual of the foreign nonprofit corporation per 13-B MRSA §104.1.B (signs at top of page 1)

## Purpose

Surrender a foreign nonprofit corporation's authority to carry on activities in Maine under 13-B MRSA §1208. Recites the foreign corporation's home jurisdiction, the date Maine authority was granted, the surrender of registered-agent authority, a post-surrender mailing address for service of process via the Secretary of State, and the principal/registered office address.

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
- Open question: Form has no widget for the signature line itself ('*By ___') — only Text7 for the printed name/capacity. Wet-ink overlay only; consistent with other Shape-D forms (MBCA-11 / MLLC-12 / CORP_MBCA-12B). Not a missing-widget bug.
- Open question: THIRD and FOURTH paragraphs are declarative recitals (revoking RA authority and consenting that termination of authority becomes effective on filing) with no widgets — they are implicitly satisfied by the act of filing. No rubric check needed beyond the signature.
- Open question: Unlike CORP_MBCA-12B, this form has no FOURTH conversion block (withdrawal.conversion.new_entity_type / governing_jurisdiction). 13-B MRSA §1208 does not provide for a withdrawal-upon-conversion path, so the conversion keys do not apply on the nonprofit surrender form.
- Open question: CORP_MBCA-12B's parallel SIXTH paragraph for principal office does NOT exist on the corporate withdrawal form — that form ends after FIFTH. NP_MNPCA-12B adds a SIXTH (principal/registered office) which is mapped to entity.principal_office.physical_address; the corporate counterpart never recites this on withdrawal.
