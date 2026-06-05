# MARK_mark4 — Application for Assignment of a Mark

**Entity type:** Trademark / Service Mark  
**Statute:** Maine Trademark Act (10 M.R.S. ch. 301-A)  
**Source:** Maine Secretary of State  
**Pages:** 5  
**Fields:** 46  
**Mapped fields:** 31  
**Filer role:** the assignor (current registrant) signs in section 3-4; the assignee dates the receipt in section 3 of part E. Each may be an individual or any of seven entity types (individual / general partnership / limited partnership / corporation / association / union / other).

## Purpose

Record the assignment (transfer of ownership) of a registered Maine trademark or service mark under 10 MRSA §1525. Recites the original mark by charter number and TEXT/FEATURES (no amendments permitted), identifies assignor and assignee with parallel entity-type/jurisdiction blocks, and captures the transfer date and signatures. The mark.* schema family is shared with MARK_mark1 (registration), MARK_mark2 (renewal), and MARK_mark6 (cancellation); this form adds mark.assignor.*, mark.assignee.*, and mark.assignment.* sub-namespaces to capture the two-party transfer pattern.

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

- `mark.assignor.name_and_address` maps to 2 widgets; all receive the same value.
- `mark.assignor.entity_type` maps to 7 widgets; all receive the same value.
- `mark.assignor.printed_name_and_capacity` maps to 2 widgets; all receive the same value.
- `mark.assignee.name_and_address` maps to 2 widgets; all receive the same value.
- `mark.assignee.entity_type` maps to 4 widgets; all receive the same value.
- Open question: mark4Twenty (rect 109.2-574.2 × 524.5-541.2 on page 1) is mapped as mark.assignment.date_of_transfer, but its width (465pt) is unusually large for a date widget. Visual inspection suggests the form text reads 'transferred on (date) ___, the entire right...' — a date interpretation. However, a '("Myself", Firm, or Corporate Name)' caption appears in the same area, hinting the widget might instead be an assignor-entity-name recital. Synth should fill with a date string and visual review at first rollout will resolve.
- Open question: Form has 6 unnamed AcroForm widgets: 3 page-1 assignee entity-type checkboxes ('individual' at y≈283.8, 'union' at y≈308.9, 'other' at y≈284.3) and 3 page-2 cover-letter expedite checkboxes (at y≈630.9 / 607.2 / 585.8). All bound by rect — filler engine must support rect-based binding for this template (same upstream issue as MARK_mark2, MBCA-10, MNPCA-10 noted in schema-gaps/2026-04-30-phase2-summary.md).
- Open question: Assignee section (E) lacks a 'Whereas, I, ___ believe' recital and lacks both a Print/Type Name and Capacity widget AND a Signature widget — only the Dated field (mark4Thirtyfive) is fillable. The assignee's signature line is wet-ink-only, and there is no separate canonical key for assignee-signer printed-name-and-capacity. This asymmetry between assignor (5 signer-related widgets) and assignee (1 date widget) is consistent with the form's role: the assignor warrants ownership and transfers; the assignee merely dates receipt.
- Open question: Form requires THREE (3) physical samples of the mark text/design to accompany the application (page-1 footer). Not captured in the AcroForm — physical attachment requirement only. No canonical key needed; rubric may verify filing.notes mentions sample submission.
- Open question: 10 MRSA §1525 requires the assignment to be recorded with the SOS within 3 months of execution (per page-0 instruction). A rubric check 'date_of_transfer within 3 months of date_signed' could enforce this, but is advisory because it depends on filing.date_received which isn't on the form.
