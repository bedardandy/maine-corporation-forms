# LLC_MLLC-1 — Application for Reservation of Name (Limited Liability Company)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** applicant (an individual or entity intending to form/qualify the LLC); applicant signs as 'applicant' on page 0

## Purpose

Reserve a name for a Maine limited liability company (domestic or foreign) for 120 days under 31 MRSA §1509.1 prior to filing a formation or qualification document. Optional election to reserve the name as an assumed/fictitious name (exempt from the LLC suffix requirement per 31 MRSA §1508).

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
- Open question: The signature line ('signature of applicant' on the lower-left) has no AcroForm widget — the only signer-related widget is Text5 ('type or print name and capacity'). Signature is collected as wet-ink/image overlay rather than via the AcroForm.
- Open question: applicant.* is a pre-formation namespace (entity does not yet exist). Reused by analogous LLP/LP/Corp reservation forms (see LLP_MLLP-1). Distinguished from filing.signer.* by representing the *requesting party* identity (could be a future LLC organizer); the signer may differ from the applicant when a corporate applicant signs through an authorized agent.
- Open question: L3C (low-profit) suffix: the form footnote includes 'L3C' and 'l3c' as valid suffixes. Rubric must accept these alongside the standard LLC suffixes.
