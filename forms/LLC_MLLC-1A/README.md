# LLC_MLLC-1A — Transfer of Reserved Name (LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 18  
**Filer role:** the original applicant (transferor) signs the transfer; transferee's consent is implicit (the transferee is named and addressed on the form but does not sign here). Single-signer Shape D — printed name and capacity combined in one widget.

## Purpose

Transfer a previously reserved LLC name from the original applicant (transferor) to a new transferee under 31 MRSA §1509.2. Records the reserved name, the original applicant's name, the transferee's name and address, and the transferor's signature. Per the page-0 note, the transfer is valid only for the remaining 120-day reservation window from the original application's filing date.

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
- Open question: The transfer expires 120 days from the date of filing of the original reservation (per the page-0 bullet). The form does not capture the original reservation's filing date — that's tracked in the SOS's records, not on this form. No canonical key needed; the 120-day window is enforced procedurally by SOS staff.
- Open question: Form has a wet-ink-only '(signature of transferor)' line on page 0 (left of the 'name and capacity' widget). No AcroForm /Tx widget binds to it — synth produces no value, and the rubric does not check for it. The transferor's typed-name-and-capacity in 'name and capacity' is the canonical signer evidence.
- Open question: The transferee's consent is not collected on this form (no transferee signature widget or block). Practically the transferee submits their own subsequent formation paperwork; this form only memorializes the transferor's release. No additional canonical keys required.
- Open question: Although categorized as 'Limited Liability Company' (form prefix MLLC), the underlying statute 31 MRSA §1509 covers reservations for LLCs, LPs, and LLLPs — sibling forms (e.g., MLPA-1A, MLLP-1A) likely follow this same shape with parallel name_reservation.* keys.
