# GP_CONV-PARTNER — Articles of Conversion of Partnership

**Entity type:** General Partnership  
**Statute:** Maine Uniform Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 21  
**Mapped fields:** 18  
**Filer role:** at least one partner OR any duly authorized representative of the converting partnership (per page-1 'Instructions For Required Signatures'); the required number of partners must have approved a plan of conversion before filing

## Purpose

Convert a Maine partnership (general partnership; LP filers use the Limited-Partnership-specific conversion form) into another entity type — Limited Partnership, Limited Liability Limited Partnership, Corporation, or Limited Liability Company — under 31 MRSA §1093. Records the converting partnership's name, the resulting entity's type and name, an exhibit of the new entity's organizing-document provisions, and an optional future effective date capped at 90 days. The corresponding formation form (MLPA-6-1, MLLC-6, or MBCA-6-1) must be attached.

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
- Open question: Form references attaching the appropriate formation form (MLPA-6-1, MLLC-6, or MBCA-6-1). filing.entities[1].name on the cover letter is likely populated with the bundled formation form's entity name (i.e., conversion.new_entity.name) for SOS routing — same pattern as MBCA-21 and MBCA-20. A canonical filing.bundled_forms[] family is not yet defined.
- Open question: The four SECOND checkboxes are unnamed (/Btn with field_id=''). Filler engine must bind by rect coordinates: top-left (Limited Partnership), bottom-left (Limited Liability Limited Partnership), top-right (Corporation), bottom-right (Limited Liability Company). The form implies mutual exclusivity ('The type of entity ... will be'), so they should be treated as a 4-way radio group.
- Open question: Form ID is GP_ (general partnership) and the form text refers generically to 'partnership'. 31 MRSA §1093 sits in the partnership-conversion provisions of Title 31. Whether LPs use this same form (vs. an LP-specific conversion form) is unclear from this PDF alone.
- Open question: Filer-role footnote on page 1 says 'at least one partner OR any duly authorized representative' — broader than the MBCA-21 'officer or duly authorized representative' shape. Synth should pick a partner or an authorized representative rather than an officer title.
