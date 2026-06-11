# MARK_mark1 — Application for Registration of a Mark

**Entity type:** Trademark / Service Mark  
**Statute:** Maine Trademark Act (10 M.R.S. ch. 301-A)  
**Source:** Maine Secretary of State  
**Pages:** 7  
**Fields:** 41  
**Mapped fields:** 33  
**Filer role:** the applicant (individual) or an officer of the applicant entity per 10 MRSA §1522.2.D — the signatory must believe the applicant is the owner of the mark and have no knowledge of conflicting senior rights

## Purpose

Register a trademark, service mark, or collective mark with the Maine Secretary of State under 10 MRSA §1522. Captures dates of first use (anywhere and in Maine), the mark's text and design features, type and class number, descriptions of goods/services and usage, applicant identity, applicant entity-type classification, and jurisdiction of incorporation/organization.

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
- Open question: MARK1 has 7 pages total per pypdf, but only pages 0, 1, 2 contain AcroForm widgets. Pages 3-6 are likely pre-filled instructions, fee schedule, MARK-5 class number reference, or mark-specimen attachment templates. Confirm by visual inspection — no canonical keys needed for non-fillable pages.
- Open question: Form references 'three (3) samples of the mark and/or design with this application' (page 1 footer) — the mark specimen attachments are physical/scanned documents, not form fields. No canonical key needed; rubric just checks filing.notes mentions specimen submission.
- Open question: Page 1 footer mentions 'Class D crime according to the Maine Criminal Code, 17-A MSEA §453, "Unsworn Falsification"' — informational only; signer affirms truthfulness implicitly.
- Open question: Page 0 fee header reads '$60 for one class, plus $10 for each additional class' — multi-class registrations are common (e.g., a single mark used on both apparel and food might register in classes 25 and 30). Class enumeration in mark.type_and_class_number should be parseable comma-separated for fee computation.
- Open question: This form uses statutory authority 10 MRSA §1522 (Title 10: Commerce and Trade), distinct from 13-C MRSA / 31 MRSA used by the entity-formation forms. The mark.* schema family is intentionally separate from entity.*; a future MARK-2 (renewal), MARK-3 (amendment), MARK-4 (assignment), MARK-6 (cancellation) will likely share most mark.* keys.
