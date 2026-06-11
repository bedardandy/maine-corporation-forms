# NP_MNPCA-12-1 — Application for Authority to Carry on Activities (Foreign Nonprofit Corporation, sub-form to accompany Application for Transfer of Authority)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 18  
**Mapped fields:** 15  
**Filer role:** authorized officer of the foreign nonprofit corporation (signature lives on the parent NP_MNPCA-12 form, not on this sub-form)

## Purpose

Page-by-page foreign-qualification disclosure block bundled with NP_MNPCA-12 (Application for Transfer of Authority) per 13-B MRSA §1202 / §1301-A. Captures the foreign nonprofit's home-jurisdiction identity, optional fictitious Maine name, jurisdiction and date of incorporation, scope of activities, and Maine registered agent. SEVENTH (registered-agent consent per 5 MRSA §108.3) and EIGHTH (certificate-of-existence within 90 days) are declarative paragraphs without widgets.

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

- `filing.seeks_full_authority` maps to 2 widgets; all receive the same value.
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- Open question: This sub-form (NP_MNPCA-12-1) lives inside the parent NP_MNPCA-12 (Application for Transfer of Authority) packet. The cover-letter primitive (filing.contact.*, filing.expedited_service, etc.) is presumed to live on the parent form, not on this sub-form's 2 pages. Confirm by inspecting NP_MNPCA-12 separately.
- Open question: No filer signature widget exists on this sub-form. The signature is presumably captured on the parent NP_MNPCA-12 — verify when reviewing that form. If the sub-form is ever filed independently, a filing.signer.* block would need to be added (template would need amendment).
- Open question: FOURTH and FIFTH free-text use the .line{1,2} convention. Synth must split a single logical purpose/activities string across the two widgets at fill time; rubric should accept either single-line or two-line input.
