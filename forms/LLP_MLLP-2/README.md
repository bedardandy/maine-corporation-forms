# LLP_MLLP-2 — Application for Registration of Name (Foreign Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 23  
**Mapped fields:** 19  
**Filer role:** a partner of the foreign LLP signing in their capacity as partner (per 31 MRSA §806-A and the page-1 footnote)

## Purpose

Register or renew the name of a foreign Limited Liability Partnership in Maine pursuant to 31 MRSA §806-A. Reserves the LLP's name in Maine for the calendar year and (per FIFTH) requires a certificate of existence dated within 90 days from the home jurisdiction. Does NOT authorize the LLP to transact business in Maine — that requires a separate Statement of Foreign Qualification.

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
- Open question: FIRST checkboxes have empty AcroForm field-ids (both at y≈434–448, distinguishable only by x-rect). Filler must bind by index/rect — same template-bug class as MBCA-10's unnamed /Btn widgets.
- Open question: Text3 and Text4 both bind to entity.principal_office.physical_address. Synth must split the address string across the two lines (or fill only Text3 if short). Rubric reads either widget.
- Open question: Page-0 fee header reads 'Filing Fee $20.00 per month' for new applications — the registration takes effect through the end of the calendar year, so a registration filed in March pays $20×10 = $200, while one filed in November pays $20×2 = $40. The fee-by-application-type rubric check encodes this prorating roughly; precise validation requires the filing.date_signed month.
