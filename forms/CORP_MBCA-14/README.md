# CORP_MBCA-14 — Certificate of Excuse (for a Maine Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 18  
**Mapped fields:** 16  
**Filer role:** any duly authorized officer OR the clerk of the corporation per 13-C MRSA §121.5 (per the page-0 footnote: 'This document MUST be signed by any duly authorized officer OR the clerk'). Sister to MBCA-14A (Certificate of Resumption) and MLLC-14B-equivalent; uses Shape D signature block (printed name and capacity).

## Purpose

File a Certificate of Excuse for a Maine domestic business corporation pursuant to 13-C MRSA §1621.4 — the simplified end-of-life procedure used when a corporation has ceased to transact business and is not indebted to the State for annual reports or fees. The body has only one substantive election (THIRD: optional non-default effective date); the FIRST and SECOND paragraphs are declarative recitals (no checkboxes), so the act of filing constitutes the certification.

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
- Open question: FIRST and SECOND paragraphs are declarative recitals (no AcroForm widgets bind to them) — confirmed against widgets.json which has only 4 page-0 /Tx widgets (141, 142, 143, 144) and zero page-0 /Btn widgets. The act of filing constitutes the certification of those recitals.
- Open question: Page-0 has a '*By ___ (signature of any duly authorized person)' wet-ink signature line (right side at y≈311) that is NOT AcroForm-bound. Only the printed-name-and-capacity widget (144) is bindable. Same convention as MBCA-14A.
- Open question: Cover-letter expedite checkboxes use field-ids 'Check Box1/2/3' rather than the more-common 'Check Box14/15/16' or the MLLC-12-style 'hold/24/imm' aliases — third observed aliasing variant. Filler engine field-id alias map should accept all three families.
- Open question: 13-C MRSA §1621.4 is the cited statutory authority for the substantive certificate; §121.5 governs who may sign. Both citations preserved in rationales for downstream rubric/synth use.
