# CORP_MBCA-6 — Articles of Incorporation

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 40  
**Mapped fields:** 36  
**Filer role:** incorporator (signs as 'original written signature' on page 2)

## Purpose

Form articles of incorporation to create a Maine domestic business corporation under 13-C MRSA, including clerk designation, share structure, board structure, optional liability/indemnification provisions, and incorporator signature.

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

- `clerk.name` maps to 2 widgets; all receive the same value.
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: Manifest contains three page-null checkboxes named 'clerk', 'sixth', 'seventh' — do these back the radio-style mutually-exclusive groups, or are they unrelated widgets pypdf could not page-locate? Inspecting pdftk dump_data_fields would confirm.
- Open question: Manifest does NOT contain a separate signature widget for the incorporator's 'original written signature' — only Text10 on the print-name row. Is the signature collected as a separate form field, or expected to be added as an image/wet-ink overlay?
- Open question: Page 1 has only 5 explicitly-paged checkboxes (Check Box28-32) but the form has visible checkboxes for SIXTH (2 options), SEVENTH (2 options), EIGHTH (3 options), NINTH (1 option), TENTH (1 option) = 9 visible. The 'sixth'/'seventh' page-null entries account for only 2; the remaining 2 may be missing widgets or shared-name groups.
- Open question: Are 'name of commercial clerk' (Text3) and 'name of clerk' (Text4) actually populated independently when filling, or does the PDF logic mirror them? If mirrored we should map only one canonical key with a fill-both copy rule.
