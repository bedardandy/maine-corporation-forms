# NP_MNPCA-11A — Statement of Intent to Dissolve (Domestic Nonprofit Corporation, Vote of Members or Directors)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 41  
**Mapped fields:** 38  
**Filer role:** any authorized officer of the corporation per 13-B MRSA §104.1.B (signs on page 1; up to two signature blocks); when adopted by member vote, the clerk/secretary or assistant secretary certifies custody of the minutes

## Purpose

File a Statement of Intent to Dissolve a Maine domestic nonprofit corporation under 13-B MRSA §1101 by *vote* (rather than written consent — written-consent variant is NP_MNPCA-11). Recites the names and addresses of the corporation's current officers (President, Treasurer, Secretary, Clerk) and up to three directors, indicates which body adopted the resolution (members vs directors when no voting members), records vote tallies (THIRD), gives the Maine registered office address (FIFTH), and is signed by an authorized officer; clerk/secretary certifies custody of the meeting minutes when the resolution was adopted by a member vote. Filing fee is $10. This filing is preliminary — Articles of Dissolution (Form MNPCA-11D or 11E) must follow.

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

- `dissolution.consent_class` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Page-1 THIRD vote-tally table has 4 widgets (Text31, Text32, Text33, Text34) but only 3 conceptual values in 13-B MRSA §1101 (entitled-to-vote, voted-for, voted-against). The most likely interpretation is that the form provides a per-class breakdown row (Text33 'Voted For' + Text34 'Voted Against') AND a totals row (Text31 'entitled to vote total' + Text32 'voted-for total'), with a missing 'voted-against total' widget. Confirm by re-rendering the PDF or by inspecting widget labels in the original template.
- Open question: Page-1 FIFTH registered-office address: Text36 (wide line below) has rect x≈327-571 (right portion only) rather than spanning the visible full-width underline. Either the bound widget covers only the right portion of a decoratively wider line, or there's a paired left-side widget that did not surface in widgets.json. Filler should populate Text36 with the full street/city/state/zip string and visually verify alignment.
- Open question: Text39 vs Text40 placement: drafter mapped Text39→clerk-cert signature and Text40→clerk-cert printed name. Reviewer corrected Text40→filing.date_signed (DATED, bottom-left narrow). Text39 (left, y≈447, narrow) is mapped to certification.clerk_signature_printed_name based on its left-side position and the inset clerk-certification box being on the LEFT, but the box's bottom signature line is conceptually below where Text39 sits — reviewer flagged for verification.
- Open question: Cover-letter filing.entities[1].name has no obvious counterpart on this single-entity filing; same generic SOS cover-letter primitive as elsewhere — likely left blank.
- Open question: FIRST table provides 3 inline director rows; additional directors must be listed on the 'reverse side' which has no AcroForm widget — overflow handled out-of-band.
