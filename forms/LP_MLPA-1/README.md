# LP_MLPA-1 — Application for Reservation of Name (Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** the applicant (the person or entity reserving the name). Distinct from filing.signer.* used on entity-amendment forms — for a name reservation, the entity does not yet exist (or, if it exists in another jurisdiction, is reserving an alternate name for Maine use), so the signer is the applicant in their own capacity, not an entity officer. Mirrors the applicant.* shape used by trademark forms (mark.applicant.*).

## Purpose

Reserve a name for a Limited Partnership in Maine for 120 days under 31 MRSA §1309.1. Captures the name being reserved, the applicant's name and address, the applicant's signature, and an opt-in checkbox indicating the name is being reserved as an assumed name (relaxes the entity-suffix requirement).

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
- Open question: The form footnote 'a reservation only acts as a reservation of the right to the use of a name. Actual use of the name is not recommended until the purpose for which the name is reserved is completed' suggests reservation alone doesn't create the LP. The 120-day window (page-0 footnote: 'Names are reserved for a period of 120 days and may not be renewed') is computed by the SOS — no expiration_date widget is present, so we don't add a canonical key for it.
- Open question: applicant.address is a single combined widget rather than the split mailing-address pattern (mailing_address.street + mailing_address.city_state_zip) used elsewhere. Kept as a single key to mirror the form's actual widget composition.
- Open question: The form does not distinguish domestic vs. foreign LP applicants. Foreign LPs reserving a Maine name (e.g., for future qualification) use the same form. No 'applicant.type' canonical key needed at pass-1.
