# CORP_CLKRA-3 — Statement of Appointment or Change of Clerk or Registered Agent

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 33  
**Mapped fields:** 28  
**Filer role:** an officer or other authorized signer per the entity-type-specific footnotes; for domestic business corps, an officer or director; for nonprofits, an officer or director; for LPs/LLPs, a general partner or duly authorized partner

## Purpose

File a statement appointing a new clerk/registered agent or changing existing clerk/RA information (address, name) for any Maine-domestic or foreign entity (corporations, LLCs, LPs, LLPs, nonprofits). Used across all entity categories.

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

- `clerk_change.action_type` maps to 2 widgets; all receive the same value.
- `clerk_change.modify_subtype` maps to 2 widgets; all receive the same value.
- `clerk_change.bc_authorization` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: This form serves multiple entity types (BC, NP, LLC, LP, LLP, foreign variants). Should fill logic require an explicit entity_type input, or infer from which fields are populated (BC fields, foreign fields, LP fields)?
- Open question: Should clerk_change.action_type and clerk_change.modify_subtype be modeled as a single hierarchical enum ('new' | 'modify.address' | 'modify.name') rather than two separate fields?
- Open question: The 'cover' (vs 'cover5') widget naming pattern repeats from MLPA-6 — confirm with SOS that this is intentional naming convention for the Immediate-expedite tier widget.
