# LP_MLPA-12 — Application for Certificate of Authority to Transact Business (Foreign Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 47  
**Mapped fields:** 45  
**Filer role:** an authorized general partner of the foreign LP (signs on page 2); when the signing GP is itself an entity, the natural-person signer fills the entity-GP signature block

## Purpose

Qualify a foreign limited partnership (LP, LLLP, or PLLLP) to transact business in Maine under 31 MRSA §1412. Records the home-jurisdiction name, an alternate Maine name when the home name lacks the required statutory suffix (FIRST), an optional fictitious-name election (SECOND), date and jurisdiction of organization (THIRD), principal-office address (FOURTH), required-office address in the home jurisdiction (FIFTH), Maine registered-agent appointment (SIXTH — commercial XOR noncommercial), the general-partner roster (EIGHTH — 3 inline rows + exhibit overflow), optional LLLP/PLLLP elections (NINTH/TENTH), and is signed on page 2 by an authorized general partner (with parallel entity-GP block).

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

- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: Page 2 signer block fixed in this review: drafter mapped Text25→general_partner_1.printed_name and Text26/Text27→general_partner_entity_1.* (per-officer pattern). Corrected to filing.signer.* / filing.signer_entity.* — the per-officer signer pattern is reserved for FORMATION filings (LP_MLPA-6 articles of LP) where there is no pre-existing entity. MLPA-12 is a foreign-qualification of an existing LP, so the signer is a 'filer-of-the-existing-entity' (Shape-B individual + entity-block parallel), matching LLP_MLLP-17 / LLP_MLLP-17A / GP_MPA-1.
- Open question: Text25's label is '(type or print name)' — Shape B (name only). The form does not ask for the GP's title/capacity in the individual block, so filing.signer.printed_name is correct; filing.signer.printed_name_and_capacity would falsify the widget shape.
- Open question: POADD2CITY field id is misleading — its rect ([105.6, 58.3, 567.6, 82.5]) is at the FIFTH-block 'mailing address if different from above' line, not a city-component. Mapped accordingly to entity.required_office.mailing_address.
- Open question: EIGHTH provides 3 inline GP rows plus an exhibit overflow checkbox; same shape as LP_MLPA-12-1.
- Open question: The (signature) and (authorized signature) lines on page 2 are wet-ink only and not bound to widgets — only the printed-name/printed-name-and-capacity widgets are bound.
