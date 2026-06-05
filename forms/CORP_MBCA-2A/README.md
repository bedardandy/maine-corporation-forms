# CORP_MBCA-2A — Consent Terminating Name Registration (Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 18  
**Filer role:** duly authorized officer of the foreign corporation

## Purpose

Terminate the registration of a foreign business corporation's name in Maine under 13-C MRSA §403.5, releasing the name so another corporation may use it. The form recites the foreign corporation's home jurisdiction, principal office address, and date of incorporation, and is signed by a duly authorized officer (per the page-1 footnote citing §1217.5).

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

- `entity.principal_office.physical_address` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Text3 and Text4 are two visual underlined lines under a single '(street, city, state and zip code)' caption — interpreted here as one address rendered across two lines. Both widgets share `entity.principal_office.physical_address`; the filler will populate either or both. A future split into `.street` / `.city_state_zip` (parallel to filing.attested_copy_recipient.mailing_address) would be cleaner, but diverges from the single-line `entity.principal_office.physical_address` convention used on MLLC-12, MLPA-12B, MLLP-12B, MLLP-12-1.
- Open question: Form has no entity-signer block (page 0 has only a single signer line). This matches CORP_MBCA-1A (the analogous corporate-name action form) — the signer is always the foreign corporation's officer signing as a natural person. No `filing.signer.entity_name` family needed here.
- Open question: 13-C MRSA §1217.5 (cited in the page-1 footnote) authorizes the signature; it does not appear to require a particular officer title (any 'duly authorized officer'). Synth may produce President/Vice-President/Secretary/Treasurer/Authorized Officer. No rubric constraint on title.
