# CORP_MBCA-20 — Articles of Nonprofit Conversion

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 18  
**Filer role:** an officer or other duly authorized representative per 13-C MRSA §933.1 (signs at bottom of page 0); shareholder approval is implicitly required by virtue of the corporation filing the articles

## Purpose

Convert a Maine domestic business corporation into a Maine nonprofit corporation under 13-C MRSA §933. Records the pre-conversion business-corporation name, the new nonprofit entity's name (which must satisfy 13-B MRSA naming requirements), an exhibit of the attached Articles of Incorporation (Form MNPCA-6-1), an optional future effective date, and an authorized signature.

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
- Open question: Form references attached Form MNPCA-6-1 (Articles of Incorporation for the resulting nonprofit). filing.entities[1].name on the cover letter is likely populated with the bundled-form's entity name for SOS routing. Cross-form bundling is also seen on MBCA-21 (MLLC-6 / MLPA-6 bundling), MLLC-12 (FICT-4 bundling), and GP_CONV-PARTNER (MLPA-6-1/MLLC-6/MBCA-6-1 bundling) — a canonical filing.bundled_forms[] family is not yet defined.
- Open question: SECOND paragraph (shareholder-approval recital) has no widget and no opt-in checkbox — unlike MBCA-10 which provides explicit shareholder-approval options. MBCA-20 implicitly assumes shareholder approval by virtue of the corporation filing the articles. No rubric check needed beyond the form-level signature.
