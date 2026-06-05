# LLC_MLLC-14A — Certificate of Resumption (for a Maine LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 17  
**Mapped fields:** 15  
**Filer role:** a person authorized by the LLC to sign per 31 MRSA §1676.1.B (signs in the bottom signature block on page 0; the form footnote requires that the signer be 'a person authorized by the limited liability company.')

## Purpose

Resume the transaction of business for a Maine domestic limited liability company that has previously suspended operations, pursuant to 31 MRSA §1665.6. Body has only three fillable widgets (entity name, dated, signer name+capacity); FIRST and SECOND are declarative-only paragraphs with no widgets. Page 1 is the standard cover-letter primitive.

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
- Open question: FIRST and SECOND on the body are purely declarative (no widgets) — FIRST recites the resumption election and SECOND recites the resumption-of-annual-reports obligation. Confirmed against widgets.json: only 3 body widgets present.
- Open question: The signature block label reads '(type or print name and capacity)' — Shape D — even though the §1676.1.B authorization is broader than 'capacity'. Mapped to filing.signer.printed_name_and_capacity for consistency with MLLC-12/MBCA-11.
