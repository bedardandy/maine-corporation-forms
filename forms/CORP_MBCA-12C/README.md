# CORP_MBCA-12C — Application for Transfer of Authority (Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 24  
**Mapped fields:** 21  
**Filer role:** officer or other duly authorized representative of the foreign corporation per §1524.1

## Purpose

Transfer a foreign business corporation's existing Maine authority into a new authority for a different foreign entity type (nonprofit corporation, LP, LLC, or LLP) following an entity-type conversion in its home jurisdiction or a re-domestication, per 13-C MRSA §1524. The form recites the original home jurisdiction and Maine authorization date, identifies the new entity type and new governing jurisdiction, and bundles the corresponding new Application for Authority (MNPCA-12 / MLPA-12 / MLLC-12 / MLLP-12) per FOURTH.

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
- Open question: FOURTH recital ('All the statements required... are attached. For a Foreign Nonprofit Corporation, attach form MNPCA-12...') has no widget — it's a fixed text block. The bundled form is implicit from transfer.new_entity_type. No `transfer.attached_authority_form_type` key needed since it would be redundant with the existing enum; rubric should infer the expected attached form from new_entity_type.
- Open question: Page-0 widgets have unusual field names — some bear the label text verbatim ('The current jurisdiction of its incorporation is', 'DATED', 'type or print name and capacity'), others use 'undefined_N' fallback. Likely a quirk of the upstream PDF authoring tool. Filler must accept these literal names; no normalization needed at this layer.
- Open question: Page 0 has no entity-signer block (only one signer line, with capacity expected to identify whether signer is 'as authorized representative of [entity]'). This matches MBCA-2A and other corporate forms; only LLP/LP forms separate the entity-signer block.
