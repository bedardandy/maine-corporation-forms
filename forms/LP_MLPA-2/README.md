# LP_MLPA-2 — Application for Registration of Name (Foreign Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 24  
**Mapped fields:** 23  
**Filer role:** general partner of the foreign limited partnership (page-1 footer: 'Application MUST be signed by at least one general partner of the foreign limited partnership. (31 MRSA §1324.1.M)'). Single-signer Shape D — printed name and capacity combined in one widget.

## Purpose

Register or renew the name of a foreign limited partnership in Maine for the calendar year under 31 MRSA §1309.2. Name registration only reserves the right to use the name in Maine; it does not authorize the partnership to conduct business in Maine (page-1 footer). Renewable annually if filed between October 1 and December 31. Requires an attached certificate of existence dated within 90 days of delivery (FIFTH). LP analog of CORP_MBCA-2 and LLP_MLLP-2.

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
- Open question: Page-0 SECOND has two address widgets (Text5 and Text6) for the principal office, with the '(street, city, state and zip code)' label below line 2. Reviewer split into entity.principal_office.physical_address.{street, city_state_zip} per MBCA-2 precedent (the corp analog of this LP form). Drafter initially mapped both to a single key — corrected.
- Open question: FOURTH ('A brief statement of the nature of the limited partnership's business') is keyed to the unscoped entity.business_purpose, NOT entity.maine_business_purpose. The page-1 footer ('The filing of this application does not authorize a limited partnership to do business in Maine') confirms the question is about the entity's general business, not a Maine-specific purpose. Drafter initially mapped to entity.maine_business_purpose — corrected.
- Open question: FIFTH (certificate of existence requirement) has no AcroForm widget — same upstream gap as MLLC-12 / MBCA-2. Tracking attachment-presence requires out-of-form metadata; rubric flags via filing.notes.
- Open question: Drafter initially proposed several schema_gaps entries for keys that already exist (entity.home_jurisdiction_name, entity.home_jurisdiction, entity.principal_office.physical_address, entity.formation_date_in_home_jurisdiction, filing.application_type). All removed in this review — these are established convention reuses, not novel proposals.
