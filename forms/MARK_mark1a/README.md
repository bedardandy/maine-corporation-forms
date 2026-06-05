# MARK_mark1a — Mark Disclaimer

**Entity type:** Trademark / Service Mark  
**Statute:** Maine Trademark Act (10 M.R.S. ch. 301-A)  
**Source:** Maine Secretary of State  
**Pages:** 1  
**Fields:** 12  
**Mapped fields:** 8  
**Filer role:** the applicant on the parent registration application — signs as 'applicant' on a wet-ink signature line. No printed-name widget on this form (only date), since the signer's printed name and capacity are captured on MARK_mark1's signature block (mark.signer.printed_name_and_capacity).

## Purpose

File a disclaimer of exclusive rights to specific portions of a trademark or service mark (text or design features) when registering a mark with the Maine Secretary of State under 10 MRSA §1521 et seq. Filed in conjunction with the primary mark-registration application (MARK_mark1) — does not stand alone, so the applicant identity and mark name live on the parent form, not on this one.

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

- `mark.type` maps to 5 widgets; all receive the same value.
- Open question: MARK_mark1a is a single-page form with no cover letter (the cover letter lives on MARK_mark1, the parent registration). No filing.entities[*], filing.contact.*, filing.expedited_service, filing.total_fees_dollars, or filing.attested_copy_recipient.* keys appear on this form — they're on the parent.
- Open question: The form's 'D' paragraph ('I understand that I may not prevent another from using the disclaimed portion...') is informational/affirmation prose, not a fillable field. No canonical key needed.
- Open question: There is a wet-ink signature line labeled '(applicant's signature)' but no AcroForm widget for the printed name on this form. The signer's printed name and capacity are captured on MARK_mark1's mark.signer.printed_name_and_capacity. If the disclaimer is ever filed standalone (rare), the signer identity would have to be inferred from context.
- Open question: Form references 'this disclaimer is filed in conjunction with' a registration application but doesn't capture a registration-application reference number — likely because both forms are submitted together in one envelope, so cross-referencing is by physical bundling, not by ID.
