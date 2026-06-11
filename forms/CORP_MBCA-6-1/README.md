# CORP_MBCA-6-1 — Articles of Incorporation (to accompany other filings)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 25  
**Mapped fields:** 23  
**Filer role:** incorporator (form has no signature widgets — signature is on the accompanying primary form, e.g., MBCA-6, MBCA-21; cover letter is also on the primary form)

## Purpose

Articles of Incorporation form designed to ACCOMPANY one of six other principal corporate filings (domestication, domestication+conversion, entity conversion, merger or share exchange, partnership conversion, or restated articles). Captures the kind of accompanying filing (mutually-exclusive enum at top of page 0), entity name, optional professional/benefit corporation elections, clerk designation, share structure, board structure, and optional liability/indemnification provisions. Filed under 13-C MRSA §202.

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

- `filing.accompanying_filing_type` binds as a single radio group `arti` with 6 options (domestication, domestication_conversion, entity_conversion, merger_or_share_exchange, partnership_conversion, restated_articles).
- `entity.professional_services_description` maps to 2 widgets; all receive the same value.
- `clerk.type` binds as a single radio group `clerk` with 2 options (commercial, noncommercial).
- `clerk.name` maps to 2 widgets; all receive the same value.
- `entity.share_structure` binds as a single radio group `class` with 2 options (single_class, multi_class).
- `entity.has_board_of_directors` binds as a single radio group `fifth` with 2 options (true, false).
- Open question: MBCA-6-1 has no signature widgets and no cover-letter widgets in widgets.json (only 2 pages). Per the form's purpose ('to accompany other filings'), the signature and cover letter belong to the primary filing (e.g., MBCA-6, MBCA-21). Synth fixture should treat MBCA-6-1 as a sub-document and reuse the parent filing's filing.date_signed / filing.contact.* fields.
- Open question: Text1 and Text2 are two consecutive full-width text widgets on page 0 immediately under the professional-corporation checkbox, followed by a single visible '(type of professional services)' label. Mapping treats them as a 2-line professional-services description (filler concatenates), parallel to MLPA-6's Text16+Text17 convention. Confirm by visual fill test.
- Open question: Page 0 widget order (by PDF y, top→bottom: y=525 → y=489 → y=465 → y=408) places professional-corporation BEFORE benefit-corporation, with the entity-name line (Text7) at y=361 — i.e., the FIRST clause appears AFTER both elective-status checkboxes on this attachment form. This differs from MBCA-6, where FIRST is at the top. Confirm by visual fill test.
