# NP_MNPCA-9 — Articles of Amendment (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 42  
**Mapped fields:** 38  
**Filer role:** any duly authorized officer of the corporation per 13-B MRSA §104.1.B (signs on page 1; up to two signature blocks)

## Purpose

Amend the Articles of Incorporation of a Maine domestic nonprofit corporation under 13-B MRSA §§802 and 803. The form captures the entity name, nonprofit type (public benefit vs mutual benefit), the inline 15-line nature-of-change/text-of-amendment block, the adoption date and method (member majority, member supermajority, written consent of all members, or board majority), the registered office address (two-line), and the authorized officer signature (two slots; only the first is required).

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

- `amendment.adoption_method` binds as a single enum_select selecting among 4 option widgets (accepted values: member_majority_at_meeting, member_supermajority_at_meeting, member_written_consent, board_of_directors_majority_vote).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: Page 1 has a 'MUST BE COMPLETED FOR VOTE OF MEMBERS' clerk-certification box ('I certify that I have custody of the minutes showing the above action by the members. (signature of clerk, secretary or asst. secretary)') with NO bound /Tx widget in the AcroForm — widgets.json shows nothing in that page-1 left-middle region. Same upstream-template glitch class as sister NP_MNPCA-11 (which DOES bind a widget for the same certification block, Text23). Filler must either skip the certification fill or treat it as wet-ink overlay. Same primitive family as MNPCA-11's certification.clerk_signature_printed_name.
- Open question: Drafter originally proposed entity.corporation_type for the FIRST public/mutual radio; corrected to entity.nonprofit_type in review to match the existing convention used on NP_MNPCA-6 / NP_MNP-6 / NP_MNP-9.
- Open question: Drafter originally proposed amendment.text mapped 15 times for widgets 4..18; corrected during review to per-line amendment.nature_and_text.line{1..15} keys to match sister NP_MNP-9's convention.
- Open question: Drafter originally mapped both registered-office widgets (24, 25) to a single registered_office.address; corrected to the address_line1 / address_line2 split that matches sister NP_MNPCA-11 / 11A / 11C.
- Open question: Drafter originally used filing.signer.printed_name_and_capacity (singular) and filing.signer_2.printed_name_and_capacity (plural-style); corrected to the indexed filing.signer_1 / filing.signer_2 pattern from sister NP_MNPCA-11 since the form provides two parallel signature slots.
