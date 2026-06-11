# LLC_MLLC-2 — Application for Registration of Name (Foreign Limited Liability Company)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 24  
**Mapped fields:** 20  
**Filer role:** an authorized person of the foreign LLC (signs page 1 in their capacity as authorized person)

## Purpose

Register or renew the name of a foreign Limited Liability Company in Maine for the calendar year under 31 MRSA §1511. Reserves the LLC's name in Maine but does NOT authorize the LLC to do business in Maine — that requires a separate Statement of Foreign Qualification (LLC_MLLC-12). Renewable annually if filed between October 1 and December 31. Per FIFTH, requires a certificate of existence dated within 90 days from the home jurisdiction (no AcroForm widget — manual attachment).

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

- `entity.principal_office.physical_address` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Drafter originally hypothesized Text8 as a certificate-of-existence date field, but FIFTH only describes the attached certificate (no fillable). Reviewer remapped the page-0 widgets to align with MLLP-2/MBCA-2/MLPA-2 conventions: Text5+Text6 = address (two-line single-key), Text7 = formation date, Text8 = business purpose. Confidence on the geometric remap is high but a single render-time visual check would confirm the underline-to-widget alignment.
- Open question: Form header reads 'Filing Fee $20.00 per month. Renewal Fee $200.00.' — the $20/month rate applies to new registrations (prorated for partial calendar years), $200 flat for renewals. The fee-by-application-type rubric handles both branches.
- Open question: FIFTH (certificate of existence) has no AcroForm widget — same upstream gap as MLLP-2/MBCA-2. Tracking attachment-presence requires out-of-form metadata.
- Open question: 31 MRSA §1676.E requires the application be signed by the person on whose behalf it is delivered (page-1 footnote). For an LLC, this is typically a member, manager, or other authorized person — capacity should match.
