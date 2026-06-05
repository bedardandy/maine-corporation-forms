# NP_MNPCA-14 — Application for Excuse (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 18  
**Mapped fields:** 16  
**Filer role:** an officer of the corporation — President, Treasurer, or Clerk/Secretary (circle title) — per 13-B MRSA §1301.5

## Purpose

Apply for excuse from filing further annual reports for a Maine domestic nonprofit corporation that has ceased to carry on activities, pursuant to 13-B MRSA §1301.5. The signer (President, Treasurer, or Clerk/Secretary — circled on the form) certifies the cessation date and that all required prior annual reports have been filed. The excuse is effective upon acceptance by the Secretary of State; if the corporation later resumes activities, annual-report filing duties resume. Filing fee is $5.

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
- Open question: The (signature) line at the bottom-right of page 0 is not bound to any AcroForm widget — wet-ink only. The 'I, ___' widget (Text2) captures only the printed name; the matching wet-ink signature is captured at fill time outside the form's machine-readable fields.
- Open question: Officer title (President/Treasurer/Clerk or Secretary) is selected by *circling* one of three printed labels rather than by checkbox or text widget. The proposed schema gap filing.signer.title_circle_choice captures the value semantically but cannot be marked on the rendered PDF — synth/rubric must handle this as an out-of-band annotation.
- Open question: Form references no exhibit and has no expedited-secondary-form bundle — single-page filing other than the cover letter.
