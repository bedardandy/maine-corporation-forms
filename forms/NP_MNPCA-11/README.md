# NP_MNPCA-11 — Statement of Intent to Dissolve (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 36  
**Mapped fields:** 36  
**Filer role:** any authorized officer of the corporation per 13-B MRSA §104.1.B (signs on page 1; up to two signature blocks)

## Purpose

File a Statement of Intent to Dissolve a Maine domestic nonprofit corporation under 13-B MRSA §1101 by written consent (members or, if no voting members, directors). Recites the names and addresses of the corporation's current officers (President, Treasurer, Secretary, Clerk) and up to three directors, indicates which class executed the written consent (SECOND), references Articles of Dissolution (THIRD), gives the Maine registered office address (FOURTH), and is signed by any authorized officer. When the consent is by member vote, a clerk/secretary certifies custody of the minutes.

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
- Open question: Page 1 widget layout fixed in this review: drafter mapped Text20→date_signed, Text22→clerk_signature, Text21/Text23→signer_1/signer_2. Actual rect positions (Text22 top-left narrow=DATED; Text20 top-right=signer_1; Text21 right-middle=signer_2; Text23 left-middle inside the certification box=clerk certification) require swapping. Corrected mappings are based on the rect coordinates and the page-1 PNG render.
- Open question: Two unnamed widgets exist on this template: an unnamed checkbox in SECOND (the 'members' option, page 0 rect [104.7, 196.3, 119.7, 211.4]) and an unnamed checkbox for the 'immediate_same_day' expedite tier on the cover letter (page 2 rect [68.7, 585.8, 90.3, 606.3]). Both have field_id='' in widgets.json. Filler must bind by rect/position rather than /T name; same upstream-template-bug class as NP_MNPCA-10's missing merged-corp signature widgets.
- Open question: FIRST table has 4 fixed officer slots (President/Treasurer/Secretary/Clerk) plus 3 inline director rows. Additional directors go to 'List additional directors on reverse side' which has no AcroForm widget — overflow has to be entered manually post-fill or omitted.
- Open question: (signature) lines next to the 'By' wet-ink anchor are not bound to widgets — only the (type or print name and capacity) widgets (Text20, Text21) are bound.
- Open question: FORM NO. MNPCA-11 (Rev. 1/23/2018) — references the older 13-B MRSA §1101 procedure (intent + later articles). The 'THIRD' recital says 'You must also file Articles of Dissolution, form MNPCA-11D or 11E' — this statement-of-intent is just step 1 of the dissolution process, not a final dissolution.
