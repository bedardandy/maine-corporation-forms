# NP_MNPCA-1 — Application for Reservation of Name (Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 19  
**Mapped fields:** 19  
**Filer role:** applicant (individual or authorized representative of the prospective entity)

## Purpose

Reserve a corporate name for a prospective Maine nonprofit corporation for 120 days under 13-B MRSA §302-A.1. The reservation does not form the entity; it only secures availability of the name. The reservation is non-renewable.

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
- Open question: Cross-form: CORP_ASUM-5 (business-corp reservation) likely uses the same applicant.* namespace. Confirm by inspection so the namespace is consistent across reservation forms (NPC, BC, LLC, LP variants if any).
- Open question: The signature line ('signature of applicant', below APPLICANT) is not an AcroForm widget — only the printed name+capacity blank is. This matches the convention on all 15 prior pass-1 forms; signatures are wet-ink overlays on rendered output.
