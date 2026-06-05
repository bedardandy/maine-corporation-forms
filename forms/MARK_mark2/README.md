# MARK_mark2 — Application for Renewal of a Mark

**Entity type:** Trademark / Service Mark  
**Statute:** Maine Trademark Act (10 M.R.S. ch. 301-A)  
**Source:** Maine Secretary of State  
**Pages:** 5  
**Fields:** 42  
**Mapped fields:** 34  
**Filer role:** the registrant (individual) or an officer of the registrant entity per 10 MRSA §1524 — must be eligible to sign a renewal application on behalf of the mark owner

## Purpose

Renew an existing Maine trademark, service mark, or collective mark registration under 10 MRSA §1524. Recites the original charter number, the original mark's text and design features (amendments to TEXT/FEATURES are NOT permitted on renewal), the type of mark (with optional amendment from the original), and any class additions or deletions. Mark.* schema family is shared verbatim with MARK_mark1 (initial registration); only renewal-specific keys (mark.charter_number, mark.type, mark.type_amended, mark.class_changes[*]) are introduced here.

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

- `mark.type_amended` maps to 2 widgets; all receive the same value.
- `mark.class_changes[0].action` maps to 2 widgets; all receive the same value.
- `mark.applicant.entity_type` maps to 5 widgets; all receive the same value.
- Open question: Form has 4 unnamed AcroForm widgets: page-1 'corporation' and 'association' entity-type checkboxes, and page-2 cover-letter '24h' and 'immediate' expedite checkboxes. All bound by rect — filler engine must support rect-based binding for this template (same upstream issue as MBCA-10 and MNPCA-10 noted in schema-gaps/2026-04-30-phase2-summary.md).
- Open question: Form has only one inline class-change row but instructs 'Complete for each class affected' — multi-class renewals must use mark.additional_pages_attached + an attachment listing further mark.class_changes[N] entries.
- Open question: TYPE-OF-MARK amendment is permitted on renewal; TEXT and FEATURES amendments are NOT (per the page-0 'B' header). Synth and rubric should respect that text_words/design_features are recitals of the original registration on this form, not editable values.
- Open question: G. 'Date of this application' uses filing.date_signed — same convention as MARK_mark1 (no separate mark.application_date key).
