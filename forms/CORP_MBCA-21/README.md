# CORP_MBCA-21 — Articles of Entity Conversion by Domestic Business Corporation

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** an officer or other duly authorized representative per 13-C MRSA §955.1 (signs at bottom of page 1)

## Purpose

Convert a Maine domestic business corporation into another type of entity (typically an LLC or LP) under 13-C MRSA §955.1, recording the corporation's pre-conversion name, the surviving entity's name and type, an exhibit of provisions required for the new public organic document, and an optional future effective date. A separate filing entity-formation form (e.g., MLLC-6 or MLPA-6) must accompany this filing.

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
- Open question: Form references attached MLLC-6 or MLPA-6 (corresponding formation forms for the surviving entity). filing.entities[1].name on the cover letter is likely populated with the bundled-form's entity for SOS routing. Cross-form bundling is also seen on MBCA-10 (FOURTH option 2 references attached MBCA-6-1) and MLLC-12 (FICT-4 bundling) — a canonical filing.bundled_forms[] family is not yet defined.
- Open question: THIRD paragraph (shareholder approval recital) has no widget and no opt-in checkbox — unlike MBCA-10 which provides explicit shareholder-approval options. MBCA-21 implicitly assumes shareholder approval by virtue of the corp filing the articles. No rubric check needed beyond the form-level signature.
