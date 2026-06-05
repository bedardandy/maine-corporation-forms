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

- `registered_agent.type` maps to 2 widgets; all receive the same value.
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: The EIGHTH 'Exhibit ___' inline blank for additional managers does not appear to be extracted as an AcroForm widget — the field that fills that role may be missing. Confirm with pdftk dump_data_fields.
- Open question: Text24 (y=250) is interpreted as the NINTH commencement-date blank, but it could alternatively be the EIGHTH Exhibit letter blank. The y-coordinate gap below the EIGHTH checkbox row suggests NINTH is correct, but this needs confirmation by filling the form and visually checking placement.
- Open question: SIXTH commercial/noncommercial radio is represented by two page-null checkboxes (Check Box15, Check Box16) — pypdf could not page-locate them. Are these separate widgets or a single radio group with shared name?
- Open question: Cover-letter expedite checkboxes are split: Check Box14 (page 3) is paired with two renamed widgets 'exp24' and 'imm' (page 3), plus two page-null Check Box15/16 leftovers. Confirm Check Box15/16 are orphaned and should be ignored at fill time.
