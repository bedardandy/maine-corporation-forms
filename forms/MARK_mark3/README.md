# MARK_mark3 — Application for Amendment of a Mark

**Entity type:** Trademark / Service Mark  
**Statute:** Maine Trademark Act (10 M.R.S. ch. 301-A)  
**Source:** Maine Secretary of State  
**Pages:** 5  
**Fields:** 43  
**Mapped fields:** 32  
**Filer role:** owner of the mark (individual, or an officer/authorized signatory of the corporate/association/union/partnership owner) per 10 MRSA §1525-A

## Purpose

Amend an existing Maine trademark/service mark registration under 10 MRSA §1525-A. Permits adding/deleting classes of goods/services and updating the owner's contact information. Page-0 instructions explicitly prohibit amending the text or design features of the mark itself — those changes require a new application (MARK-1). Captures (A) charter number of the existing registration, (B) a recital of existing text and design features, (C) current type of mark and a yes/no for whether the type is being amended, (D) class number being added/deleted plus description of goods/services and manner of use, (E-F) a refreshed applicant identity block (name, mailing address, entity type, jurisdiction, formation date), (G) date of application, and a single signer block. 3 pages, 45 widgets.

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

- `mark.type_changed` maps to 2 widgets; all receive the same value.
- `amendment.class_action` maps to 2 widgets; all receive the same value.
- `amendment.manner_of_use` maps to 3 widgets; all receive the same value.
- `mark.applicant.entity_type` maps to 6 widgets; all receive the same value.
- `filing.expedited_service` maps to 2 widgets; all receive the same value.
- 1 low-confidence mapping(s) need human review: `mark.type_change_explanation`
- Open question: Reviewer corrected three classes of drafter errors: (a) drafter put applicant identity fields under the entity.* namespace (entity.name, entity.mailing_address, entity.type, entity.home_jurisdiction, entity.formation_date) — corrected to mark.applicant.* per the MARK-1 precedent (mark owners are not necessarily registered Maine entities, and 10 MRSA Title 10 marks are intentionally namespaced separately from 13-C/31 MRSA entity-formation forms); (b) drafter mapped the signer to filing.signer.printed_name_and_capacity — corrected to mark.signer.printed_name_and_capacity per MARK-1; (c) drafter omitted mark3Six (rect 165.8, 298.7, 296.7, 317.0) — added with provisional key mark.type_change_explanation and confidence='low' pending visual confirmation.
- Open question: mark3Five and mark3Six are two text fields between TYPE OF MARK (mark3Four) and the yes/no checkbox pair. mark3Five (full-width) is interpreted as an 'original type, if changed' recital line; mark3Six (smaller, ~131x18pt) is interpreted as a sub-question/explanation prompt. Both interpretations are tentative — pass-1 leaves them as best-guess provisional keys; a pass-2 visual check or a single test fill will confirm whether they need different keys (e.g., mark3Five could be a free-form note line, and mark3Six could be unrelated to type-change).
- Open question: amendment.manner_of_use is a 3-line widget primitive (Text13/14/15). MARK-1's analogous mark.usage_description is a 2-line primitive (line1/line2 sub-keys). The MARK-3 form gives 3 rows for the same concept; canonical key collapses all three into a single string with synth concatenating non-empty lines (consistent with MLPA-6's professional-services pattern), avoiding a per-line sub-key explosion.
- Open question: Two unnamed widgets are preserved with empty field_id as upstream: page 1 'association' checkbox at rect [68.1, 534.5, 85.6, 550.6] and page 2 'Immediate expedited filing' checkbox at rect [68.7, 585.8, 90.3, 606.3]. Same convention as ASUM-5.
- Open question: Form references 10 MRSA §1525-A (mark amendment statute, distinct from §1522 used by MARK-1 registration). Page-0 header explicitly prohibits amending the text/design of the mark itself — only classes and applicant contact info are amendable. Rubric does not enforce this directly (no widget for amended-text), but synth/UI should warn users who try to use this form to change a mark's text or design.
