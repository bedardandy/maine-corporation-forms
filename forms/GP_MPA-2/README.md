# GP_MPA-2 — Statement of Dissolution (General Partnership)

**Entity type:** General Partnership  
**Statute:** Maine Uniform Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 19  
**Mapped fields:** 17  
**Filer role:** any partner of the general partnership (individual or entity); see 31 MRSA §1005.3

## Purpose

File a Statement of Dissolution under 31 MRSA §1085 declaring that a Maine general partnership has dissolved and is winding up its business. Recites the partnership name (FIRST), the dissolution-and-winding-up declaration (SECOND), and an under-penalty-of-perjury attestation (THIRD); signed on page 0 by an authorized partner per 31 MRSA §1005.3 (individual or entity-partner).

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
- Open question: Signer block fixed in this review: drafter mapped Text3→partner_1.printed_name and Text4/Text5→partner_entity_1.* (per-officer pattern). Corrected to filing.signer.* / filing.signer_entity.* — the per-officer signer pattern is reserved for FORMATION filings (LP_MLPA-6, MNPCA-6, MBCA-6) where the signers are originators of a brand-new entity. GP_MPA-2 is a post-formation statement on an existing partnership, so the signer is a filer of the existing entity — same pattern as GP_MPA-1 (Statement of Dissociation sibling).
- Open question: Text3's label is '(type or print name)' — Shape B (name only). filing.signer.printed_name is correct; collapsing to printed_name_and_capacity would falsify the widget shape.
- Open question: Individual block (Text3) and entity block (Text4/Text5) are alternatives — the form layout makes them mutually exclusive but does not enforce it via a radio. Captured as an exactly-one rubric check.
- Open question: The (signature) and (authorized signature) lines have no AcroForm widgets — wet-ink signatures expected at fill time.
