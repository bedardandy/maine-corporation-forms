# LLP_MLLP-5A — Termination of Statement of Intention to Do Business Under an Assumed or Fictitious Name (LLP)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 18  
**Filer role:** a partner of the LLP (individual or entity) signing per 31 MRSA §805-A.8 — page-0 footnote requires '*Certificate MUST be signed by at least one partner'

## Purpose

Terminate a previously filed Statement of Intention to do Business Under an Assumed or Fictitious Name for a Maine Limited Liability Partnership under 31 MRSA §805-A.8 and §860-A. Captures the LLP's real name, the assumed/fictitious name being terminated, and a single signer block (individual partner OR entity partner).

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
- Open question: Form has only ONE inline partner-signer slot and ONE inline entity-partner-signer slot — single-slot signer pattern, not multi-slot. Reviewer corrected drafter's partner_N.* / partner_entity_N.* mapping (which would be appropriate for forms like MLLP-6A with 2 inline slots) to filing.signer.* / filing.signer_entity.* (matching MLLP-9 / GP_MPA-1).
- Open question: Page-0 has no widget for a checkbox indicating whether the original Statement of Intention has additional contextual information (e.g., the date the original fictitious name was filed). 31 MRSA §805-A.8 may require disclosure of the original filing date — confirm whether this is required upstream and, if so, whether it should be a new schema_gap or attached as an exhibit.
- Open question: Field-id naming uses the bare '5a1'/'5a2'/... convention (form-id-prefixed digit) rather than the more common 'TextN'/'Check BoxN' pattern. Same template style as GP_MPA-1's 'cover1'/'cover2' pattern. Confirm filler engine handles non-prefixed field-ids correctly.
