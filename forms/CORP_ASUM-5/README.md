# CORP_ASUM-5 — Statement of Intention to Do Business Under an Assumed Name

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 24  
**Mapped fields:** 21  
**Filer role:** an authorized officer/clerk/partner/manager/member of the entity per the entity-type-specific signature footnotes (BC §1121, NP §1121, LLC §1531, LP §108.3, LLP §1024). When the signing partner is itself an entity (LP/LLP only), the entity name goes in the LIMITED PARTNERSHIPS section; the natural person who signs on behalf of that entity uses the (type or print name) field above.

## Purpose

Register an assumed name (DBA) for an existing Maine domestic or foreign-qualified entity (corporation, LLC, LP, LLP, nonprofit). Captures the entity's exact legal name, the assumed name, the location(s) where the assumed name will be used, and (for foreign entities only) jurisdiction of origin and Maine authorization date. Filing fee is entity-type-specific: $125 for-profit, $25 nonprofit (per page 0 header).

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
- Open question: Page 0 has a '*By _________' line above the (type or print name) widget that is the actual signature line on the form. No corresponding AcroForm widget exists for it (template gap). Synth fills printed_name + title only; the handwritten signature is applied post-print.
- Open question: Two unnamed widgets exist (field_id ''): the Exhibit-letter inline blank on page 0 (rect [308.0, 396.1, 333.1, 417.8]) and the second cover-letter entity row on page 1 (rect [36.5, 675.1, 472.9, 697.6]). Fill engine matches these by rect/widget index. If the engine requires unique field_ids, upstream PDFs need patching.
- Open question: Form serves all entity types (BC, NP, LLC, LP, LLP, foreign variants) — entity_type is not captured on the form itself. Fee validation and signer-title constraints depend on entity_type, which must be supplied externally (e.g., via the filing's metadata).
- Open question: Entity-type-specific signature footnotes (*1)–(*5) on page 0 enumerate which titles are valid per entity type (e.g., for a BC the signer must be '(an officer)' per 13-C §1121.1). Rubric should validate filing.signer.title against entity_type when entity_type is available.
