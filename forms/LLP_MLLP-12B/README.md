# LLP_MLLP-12B — Cancellation of Authority to Do Business (Foreign Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 23  
**Mapped fields:** 23  
**Filer role:** at least one partner of the foreign LLP, OR any duly authorized person (individual or authorized representative of an entity signer)

## Purpose

Cancel a foreign LLP's authority to do business in Maine under 31 MRSA §857. Captures the LLP's home-jurisdiction name, the Maine name (if different) used at qualification, the home jurisdiction, the original Maine authorization date, and the principal/registered office address. Signed by at least one partner OR any duly authorized person per the page-1 footnote.

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
- Open question: FIRST collapses §853.1.A (fictitious-name) and §852.2.B (assumed-name-for-suffix) into a single widget, while MLLP-12 (qualification) keeps them as separate widgets keyed entity.maine_fictitious_name and entity.maine_assumed_name_for_suffix. The cancellation form has no way to disambiguate which path was used at qualification — pass-1 maps the widget to entity.maine_fictitious_name (the more general 'Maine name when different' key); a cleaner long-term fix would be a coalesced entity.maine_qualification_name view that resolves to whichever original key is non-empty.
- Open question: Page 0 has no widget for FOURTH/FIFTH (textual recitals about cancellation effect and dissolution-in-home-jurisdiction) — these are fixed paragraphs without filer input, which matches the pattern on MLPA-12B.
- Open question: Page 1 footnote permits 'at least one partner OR any duly authorized person' — looser than the LP per-officer-signer pattern. This is why the form uses the generic filing.signer.* family instead of partner_N.* keys. Consistent with MLLP-12 (qualification) and MLLP-17 (correction).
