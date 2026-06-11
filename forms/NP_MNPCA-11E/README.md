# NP_MNPCA-11E — Voluntary Dissolution by Incorporators (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 22  
**Mapped fields:** 22  
**Filer role:** majority of the incorporators (page-1 footnote: '*This document MUST be signed by a majority of the incorporators'). Up to 3 incorporator slots inline; overflow not bound by AcroForm widgets.

## Purpose

Dissolve a Maine domestic nonprofit corporation by incorporator consent under 13-B MRSA §1101-A. This dissolution path is available only when (per the form's recitals) the corporation has not carried on activities (SECOND), no debts remain unpaid (THIRD), a majority of incorporators consent to dissolve (FOURTH), and all required Annual Reports have been filed with the SOS (FIFTH). Captures the entity name, original articles filing date (FIRST), Maine registered office (SIXTH, two-line), and up to three incorporator signatures with name+capacity (page 1). Filing fee $10 per page-0 header.

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

- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: The form provides 3 inline incorporator slots but the page-1 footnote requires a 'majority' of all incorporators to sign — for a corporation with more than 3 incorporators originally, the 3-slot limit is insufficient and overflow is not bound to any AcroForm widget. The §1101-A path is intended for never-activated corporations (typically with few incorporators), so this is unlikely to bind in practice — but rubric cannot fully verify majority without out-of-band knowledge of the total incorporator count from the original articles.
- Open question: FIFTH paragraph requires that 'All required Annual Reports have been filed with the Secretary of State' — this is a recital with no widget. SOS staff verify against their own records. Not a rubric-actionable field but a precondition for filing.
- Open question: FIRST widget (11e2) is narrow (rect width ≈110, x=308..418) — sized for a date string only. SECOND/THIRD/FOURTH/FIFTH paragraphs are pure recitations with no widgets. This is a 'recitation-with-minimal-blanks' pattern: incorporators attest by signing that all the statutory preconditions (no activities, no debts, majority consent, annual reports filed) are met.
- Open question: *By signature lines on page 1 are decorative — not bound to AcroForm widgets. Each signer block has only one bound widget (the '(type or print name and capacity)' line). Wet-ink signatures applied post-print.
