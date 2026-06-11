# LLC_MLLC-14 — Certificate of Excuse (for a Maine LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 17  
**Mapped fields:** 17  
**Filer role:** a person authorized by the LLC to sign per 31 MRSA §1676.1.B (signs in the bottom signature block on page 0; the form footnote requires that the signer be 'a person authorized by the limited liability company.')

## Purpose

File a Certificate of Excuse for a Maine domestic LLC under 31 MRSA §1665.5, certifying that the company has ceased to transact business and is not indebted to the State for annual reports or fees. Body has only three fillable widgets (entity name, dated, signer name+capacity); FIRST and SECOND are declarative-only paragraphs with no widgets. Page 1 is the standard cover-letter primitive. Sibling to MLLC-14A (Resumption) under §1665.6.

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
- Open question: FIRST and SECOND on the body are purely declarative (no widgets) — FIRST recites the cessation-of-business election and SECOND recites the no-debt-to-State certification. Confirmed against widgets.json: only 3 body widgets present.
- Open question: The signature block label reads '(type or print name and capacity)' — Shape D — even though the §1676.1.B authorization is broader than 'capacity'. Mapped to filing.signer.printed_name_and_capacity for consistency with MLLC-12, MLLC-14A, MBCA-11.
- Open question: No widget exists for the actual signature line above the printed name; signature is wet-ink/image overlay (consistent with all other Maine SOS LLC forms).
