# NP_MNPCA-13A — Amended Annual Report (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 27  
**Mapped fields:** 25  
**Filer role:** duly authorized officer of the nonprofit per 13-B MRSA §104.1.B (signs at the top of page 1)

## Purpose

File an amended annual report for a Maine nonprofit corporation under 13-B MRSA §1301-C, correcting or updating information previously reported. Recites the home jurisdiction, the date the original annual report was filed, the substantive changes (free-text, up to 7 inline lines), and the effective date of those changes. The amendment window runs from the original filing date through December 31 of the same filing year.

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
- Open question: The signature line itself (under '*By ___ (authorized signature)') has no AcroForm widget — wet-ink only. Same Shape-D convention as MBCA-11 / MLLC-12 / MBCA-12; the printed-name-and-capacity widget is the bound field.
- Open question: If officer or director information is being changed (per the page-0 instructions), the amendment must include name, title, and complete physical address — but the form provides only 7 free-text lines for this. There is no structured officer_N.* roster on this form; the synth builder must inline that data into amendment.changes_description.line{1..7} as prose, and the rubric cannot validate it structurally.
