# CORP_MBCA-14A — Certificate of Resumption (for a Maine Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 21  
**Filer role:** any duly authorized officer of the corporation per 13-C MRSA §121.5 (the page-0 footnote states 'this document MUST be signed by any duly authorized officer of the corporation'). Sister form to MLLC-14A but uses Shape D signature block (printed name and capacity) and adds the FIRST/SECOND/THIRD body widgets that MLLC-14A lacks.

## Purpose

Resume the transaction of business for a Maine domestic business corporation that has been suspended or forfeited, pursuant to 13-C MRSA §1621.5. The filer must certify that shareholders authorized the resumption — either (a) by majority vote at a meeting (with date and location recited) or (b) by written consent — and may optionally specify an effective date other than the date of filing (THIRD).

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
- Open question: Form has 8 body widgets on page 0 (entity name, two FIRST checkboxes, meeting date, meeting location, THIRD effective date, DATED, signer name+capacity). The '*By' signature line on the bottom row is visible on the rendered form but is NOT AcroForm-bound — wet-ink only. Confirmed against widgets.json: only widgets at y=231/190/156, no signature widget at y≈190 right side.
- Open question: Cover-letter widgets use template-specific field-id aliases ('hold', '24', 'imm') instead of the more-common 'Check Box14/15/16'. Same convention as LLC_MLLC-12. Filler engine should already handle these via the field-id alias map documented in schema-gaps/2026-04-30-cover-letter-primitive.md.
- Open question: Cover-letter row 1 uses field-id 'Name of entitys on the submitted filings 1' (with the same template-typo as row 2's 'Name of entitys on the submitted filings 2'). Most other forms use 'Name of entity' for row 1 — add this alias to the field-id rename map.
- Open question: 13-C MRSA §1621.5 is the cited statutory authority; the form footnote also references §121.5 for officer-signing authority. Both citations preserved in rationales for downstream rubric/synth use.
