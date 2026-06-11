# NP_MNPCA-11C — Statement of Revocation of Voluntary Dissolution Proceedings (Domestic Nonprofit, Vote of Members or Directors)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 36  
**Mapped fields:** 35  
**Filer role:** any duly authorized officer of the corporation per 13-B MRSA §104.1.B (signs on page 1; up to two signature blocks); when adopted by member vote, the clerk/secretary or assistant secretary certifies custody of the minutes

## Purpose

Revoke previously authorized voluntary dissolution proceedings for a Maine domestic nonprofit corporation under 13-B MRSA §1102, based on a vote of the members (or directors when there are no voting members). Records the corporation's current officers (President, Treasurer, Secretary, Clerk) and up to three directors, indicates which body voted to revoke (SECOND), gives the Maine registered office address (THIRD), and is signed by an authorized officer; clerk/secretary certifies custody of the meeting minutes when the revocation was adopted by a member vote. Filing fee is $5. The resolution authorizing revocation must be attached as Exhibit A.

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
- Open question: Page 1 inset 'MUST BE COMPLETED FOR VOTE OF MEMBERS' clerk-certification box has a visible signature line for 'signature of clerk, secretary or asst. secretary' but NO AcroForm widget binds to it — only widgets 20 (DATED), 21 (signer_1), and 22 (signer_2) exist on page 1. This is a template-level upstream issue: when revocation.consent_class='members', the user must wet-ink-sign the clerk-cert line, which the filler engine cannot pre-populate. Same primitive family as sister NP_MNPCA-11's certification.clerk_signature_printed_name, but here unbound.
- Open question: FIRST roster has 3 inline director rows; additional directors must go on the 'reverse side' (no AcroForm widget) — overflow handled out-of-band.
- Open question: Cover-letter filing.entities[1].name has no obvious counterpart on this single-entity filing; same generic SOS cover-letter primitive as elsewhere — likely left blank.
- Open question: Drafter originally proposed officer_N.printed_name_and_capacity for the roster; reviewer corrected to role-keyed officer_<role>.name + officer_<role>.address (with director_N.* for the indexed director rows) to match the sister NP_MNPCA-11 convention. The form's column header is 'Title | Name | Address', so name and capacity are NOT combined in a single widget — capacity is supplied by the printed row label.
