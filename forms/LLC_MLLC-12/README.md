# LLC_MLLC-12 — Statement of Foreign Qualification (Foreign LLC Authority to Conduct Activities)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 44  
**Mapped fields:** 40  
**Filer role:** authorized signatory of the foreign LLC (signs at bottom of page 2)

## Purpose

Qualify a foreign limited liability company to conduct activities in Maine under 31 MRSA §1622, providing home-jurisdiction info, alternate/fictitious Maine name (if needed), Maine registered agent, manager list, commencement date, optional professional/series-LLC elections, and a certificate of existence.

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
- Open question: The EIGHTH 'Exhibit ___' inline blank for additional managers does not appear to be extracted as an AcroForm widget — the field that fills that role may be missing. Confirm with pdftk dump_data_fields.
- Open question: Text24 (y=250) is interpreted as the NINTH commencement-date blank, but it could alternatively be the EIGHTH Exhibit letter blank. The y-coordinate gap below the EIGHTH checkbox row suggests NINTH is correct, but this needs confirmation by filling the form and visually checking placement.
- Resolved: the SIXTH commercial/noncommercial choice is two independently named checkboxes on page 1 (Check Box15 next to "Commercial Registered Agent", Check Box16 next to "Noncommercial Registered Agent", each with on-state Yes — verified by geometry+text). `registered_agent.type` binds them as an enum_select so exactly one box is ever marked; they are not cover-letter leftovers (the page-3 expedite boxes are 'exp24' and 'imm').
