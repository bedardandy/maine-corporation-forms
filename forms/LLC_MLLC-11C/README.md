# LLC_MLLC-11C — Certificate of Cancellation (Domestic LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 23  
**Mapped fields:** 19  
**Filer role:** person authorized by the LLC (or person winding up activities if dissolved with no members) per 31 MRSA §1676.1.B/C; signs the body of page 0 over the *Authorized Signature** caption

## Purpose

Cancel a Maine domestic limited liability company under 31 MRSA §1533.2 (and 31 MRSA §1676.1.B/C for the signer). Records (FIRST) the date the original certificate of formation was filed, (SECOND) the date the LLC was dissolved (if known), (THIRD) the cancellation effective-date election (date of filing OR a future date), (FOURTH) any additional information set forth in an exhibit, and a single signer block with date and printed-name-and-capacity. Filing fee is $75 per the page-0 header. 2 pages, 24 widgets — page 1 is the standard cover-letter primitive.

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
- Open question: Two unnamed widgets on page 0 (rect [102.1, 409.0, 117.1, 424.1] and [101.5, 384.1, 116.4, 399.3]) carry the THIRD checkbox-pair semantics (date_of_filing XOR future_date). Field-id is empty in widgets.json — fill engine matches by rect/widget index. If the engine requires unique field_ids, upstream PDF needs patching.
- Open question: Text4 (rect [426.7, 458.2, 567.5, 478.8]) is the *Authorized Signature** wet-ink line. Same convention as ASUM-5: form lists a /Tx widget at the signature underline but SOS expects a handwritten or scanned-image signature, not typed text. Excluded from canonical-key assignment (set to null); flagged here.
- Open question: Page-0 footnote cites 31 MRSA §1676.1.B (authorized person) or §1676.1.C (person winding up if no members). Capacity in filing.signer.printed_name_and_capacity should reflect one of these — e.g., 'John Doe, Authorized Person' or 'Jane Smith, Person Winding Up'. Rubric does not enforce specific capacity strings; left to synth/UI to constrain.
