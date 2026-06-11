# NP_MNP-9 — Certificate of Amendment (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 35  
**Mapped fields:** 35  
**Filer role:** secretary or clerk of the corporation (per 13-B MRSA §934 footnote: 'This document MUST be signed by the secretary or clerk of the corporation')

## Purpose

File a Certificate of Amendment to amend the articles of organization of a Maine domestic nonprofit corporation under 13-B MRSA §934. Captures entity name, nonprofit type (public-benefit vs mutual-benefit), the inline nature-and-text of the amendment (15-line free-text block), the adoption date and method (member vote vs board/managing-board vote), and the secretary/clerk authorized signature.

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

- `entity.nonprofit_type` binds as a single radio group `bene` with 2 options (public_benefit, mutual_benefit).
- `amendment.adoption_method` binds as a single radio group `vote` with 2 options (member_vote, board_vote).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: FIRST and THIRD radio groups are represented by 4 unnamed /Btn-style widgets in the AcroForm (no /T name, page-located). Confirm with pdftk dump_data_fields whether they are /Btn checkbox widgets backing the radio groups, or decorative widgets that the filler must bind by index/rect rather than name. Same concern as MBCA-10 (3 unnamed page-1 election checkboxes).
- Open question: The amendment text area is 15 separate /Tx widgets (Text12, Text14, Text15, Text16–Text27) with non-sequential widget numbering but contiguous y-coordinate ordering. Filler must distribute long text across lines by y-position, not widget index. Confirm whether the PDF originally had a single multi-line /Tx that was split during template revision, or whether the 15 widgets are intentional.
- Open question: Form is named 'MNP-9' (no 'CA' suffix) — distinct from the namespacing convention used by MNPCA-6 / MNPCA-10 / MNPCA-12 (those use 'MNPCA-N'). The 'MNP-N' prefix may indicate a different revision lineage (footer dated 4/14/2014). Document the dual prefix convention in pass-2 to avoid synth/rubric collisions.
- Open question: Form footnote requires signature by 'secretary or clerk', but the AUTHORIZED SIGNATURE block has no separate widget for the wet-ink signature line — only Text29 (DATED) and Text38 (printed name+capacity). Confirm whether the signature is collected as wet-ink overlay (no AcroForm widget) or whether a signature widget was omitted from the template.
