# LLP_MLLP-1 — Application for Reservation of Name (Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** applicant (an individual or entity intending to form/qualify the LLP); applicant signs as 'applicant' on page 0

## Purpose

Reserve a name for a Limited Liability Partnership (LLP) in Maine for 120 days under 31 MRSA §804-A.1, prior to filing the LLP's qualification statement. Optional election to reserve the name as an assumed/fictitious name (exempt from the LLP suffix requirement).

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
- Open question: The signature line ('signature of applicant' on the lower-left) has no AcroForm widget — the only signer-related widget is one6 ('type or print name and capacity'). Signature is collected as wet-ink/image overlay.
- Open question: Field naming: this template uses 'one2', 'one3', ..., 'one6' rather than 'TextN' prefix. Filler should accept multiple naming styles; same caveat as NP_MNPCA-10A and other older templates.
- Open question: All schema_gaps for this form (applicant.name, applicant.address, filing.is_assumed_name_reservation) are first introduced on the LLC reservation form (LLC_MLLC-1) and reused unchanged here — no new keys unique to LLP_MLLP-1.
