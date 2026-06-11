# LLP_MLLP-12A — Amended Application for Authority to Do Business (Foreign LLP)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 28  
**Mapped fields:** 28  
**Filer role:** at least one partner OR any duly authorized person of the foreign LLP, signing under the bottom-of-page-1 footnote 'Certificate MUST be signed by (1) at least one partner OR (2) any duly authorized person.' Two parallel signature blocks: an individual block (Partner(s)*) and an entity block (For Partner(s) which are Entities) — exactly one is populated per filing.

## Purpose

Amend the authority of a foreign LLP to do business in Maine under 31 MRSA §855 (sibling of MLLC-12A for foreign LLCs and CORP_MBCA-12A for foreign corporations). Updates may include the home-jurisdiction name (FIRST), the Maine fictitious name and accompanying FICT-4 (SECOND), the nature of business (THIRD), the principal-office address (FOURTH), and the contact partner's name/address (FIFTH). SIXTH allows an exhibit-attached catch-all for other amendments. Each amendment paragraph follows the standard 'If no change, so indicate.' convention — empty values mean no change to that item.

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
- Open question: Page-0 header annotation reads 'Filing Fee $90.00 — (If amending ONLY Item FOURTH and/or Item FIFTH the filing fee is $35.00.)'. The fee depends on which paragraphs were amended; a rubric helper would need to inspect which keys carry non-'No change' values to compute the correct base.
- Open question: Pages-0/1 do not include a 'certificate of existence' (COE) attached checkbox like LLP_MLLP-1 / MLLC-12 do. Whether a COE is statutorily required for an amended LLP application under §855 is unclear — open question for upstream review (cf. CORP_MBCA-12A, which DOES require a COE when the home jurisdiction changes).
- Open question: FIFTH provides only a single contact-partner row (Name + Address widgets). Unlike LLP_MLLP-1's EIGHTH paragraph, there is no overflow opt-in for additional contact partners. If a filer needs to update multiple contact partners, the only mechanism is the SIXTH 'other amendments' exhibit.
- Open question: Page-1 (signature) line below 'Partner(s)*' has no AcroForm widget — only 12a12 for printed name + capacity. Same for the entity-signer block: 12a14 holds the printed name + capacity, the (authorized signature) line is wet-ink only.
- Open question: FIRST through FIFTH each include 'If no change, so indicate.' — the form expects either a literal 'No change' marker or the new value. Synth/rubric must accept either: empty OR 'No change' both mean 'no amendment' for that paragraph.
