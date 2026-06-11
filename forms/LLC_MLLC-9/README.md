# LLC_MLLC-9 — Certificate of Amendment (Maine Limited Liability Company)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 32  
**Mapped fields:** 28  
**Filer role:** authorized person(s) of the LLC per 31 MRSA §1676.1 — at least one signature required, two inline slots provided

## Purpose

Amend the certificate of formation of a Maine domestic limited liability company under 31 MRSA §1532 (Filing fee $50). Captures the LLC's current legal name (top), an optional new name (FIRST), the date of the original certificate of formation (SECOND), low-profit LLC designation (THIRD per 31 MRSA §1611), professional LLC designation with services description (FOURTH per 13 MRSA Chapter 22-A), an optional registered-agent change (FIFTH/SIXTH — commercial XOR noncommercial; 'Complete only if there is a change to the registered agent information'), and other amendments via exhibit (SEVENTH). Page 2 has a dual-signer block ('Authorized person(s)') — per **31 MRSA §1676.1, the certificate must be signed by a person authorized by the LLC; the form provides 2 inline slots so either one or two authorized persons may sign. Page 3 carries the standard cover-letter primitive.

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
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: FIFTH section header reads 'Complete only if there is a change to the registered agent information' — there is NO opt-in checkbox indicating an agent change. Synth/rubric infers presence from the populated keys. A future cleanup might add an `entity.registered_agent_change` boolean alongside, but no widget exists today.
- Open question: Two name slots Text10 (commercial path) and Text11 (noncommercial path) both bind to registered_agent.name with the convention that exactly one is filled based on registered_agent.type. Identical pattern to LP_MLPA-12-1 Text12/Text13.
- Open question: Text6 / Text7 both belong to entity.professional_services_description; split into .line1/.line2 to mirror the multi-line shape primitive (same as LP_MLPA-12-1 and amendment.changes_description.lineN on MLPA-13A).
- Open question: Page 2 has two parallel signer rows ('Authorized person(s)' header is plural). Mapped to authorized_person_{1,2}.printed_name_and_capacity per the LLC_MLLC-6A pattern. §1676.1 requires only one signer; the second slot is optional.
- Open question: The drafter initially mis-aligned page-1 widgets (Text7 → registered_agent.name, Text13 → cra_public_number, etc.). Reviewer corrected by re-reading the rendered page — Text7 is the second professional-services line; Text14 alone is the CRA Public Number alongside the commercial radio.
