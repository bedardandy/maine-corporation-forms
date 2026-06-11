# CORP_MBCA-2 — Application for Registration of Name (Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 24  
**Mapped fields:** 23  
**Filer role:** duly authorized officer of the foreign corporation (signs at bottom of page 0)

## Purpose

Register or renew the name of a foreign business corporation in Maine for the calendar year under 13-C MRSA §403. Name registration only reserves the right to use the name in Maine; it does not authorize the corporation to conduct business in Maine (which requires a separate Statement of Foreign Qualification, MBCA-12). Renewable annually if filed between October 1 and December 31.

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

- `filing.application_type` binds as a single enum_select selecting among 2 option widgets (accepted values: new, renewal).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: MBCA-2 introduces the multi-widget split variant entity.principal_office.physical_address.{street, city_state_zip}, vs MLLC-12's single-line entity.principal_office.physical_address. Both shapes are now in pass-1 — synth/rubric should branch by form_id (or expose a helper that accepts both).
- Open question: FIFTH (certificate of existence requirement) has no AcroForm widget — same upstream gap as MLLC-12's TWELFTH. Tracking attachment-presence requires out-of-form metadata.
- Open question: entity.business_purpose is a new namespace key vs MLLC-12's entity.maine_business_purpose. If a future review decides to unify them, the unification should preserve the Maine-scoped vs unscoped semantic distinction (e.g., entity.business_purpose with an optional jurisdiction qualifier).
