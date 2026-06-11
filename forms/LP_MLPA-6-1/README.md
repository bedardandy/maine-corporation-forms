# LP_MLPA-6-1 — Certificate of Limited Partnership — accompanying a transaction (Conversion / Merger / Consolidation)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 28  
**Mapped fields:** 21  
**Filer role:** (none on this sheet) — the certificate of limited partnership is signed on the accompanying transaction filing's signature block; this 2-page form has no signature widget and no date widget

## Purpose

Form a Maine domestic limited partnership under 31 MRSA §1321 in connection with one of five accompanying transactions (Articles of Entity Conversion, Articles/Certificate of Merger or Share Exchange, Certificate of Inter-Entity Consolidation, Articles/Certificate of Conversion, Articles of Conversion of Partnership). The form (2 pages, 28 widgets) captures: a five-option transaction-type election (top of page 1, 'X one box only'), the LP name with required suffix (FIRST), designated-office physical/mailing addresses (SECOND), Maine registered-agent appointment (THIRD — commercial XOR noncommercial; FOURTH paragraph confirms agent consent), the general-partner roster (FIFTH — 3 inline rows + exhibit overflow), optional LLLP elect-in (SIXTH), optional PLLLP elect-in plus 2-line professional-services description (SEVENTH), and an optional additional-provisions exhibit letter (EIGHTH). There is no cover letter, no signature block, and no date_signed widget on this form — those live on the accompanying transaction filing (e.g., MBCA-21, MLPA-9, MLPA-17) that this form bundles with. Same '-1' bundled-sheet pattern as LP_MLPA-12-1 and LLP_MLLP-12-1.

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

- `filing.accompanying_transaction_type` maps to 5 widgets; all receive the same value.
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `entity.professional_services_description` maps to 2 widgets; all receive the same value.
- Open question: MLPA-6-1 has only 28 widgets (2 pages) — no cover-letter primitive, no signature block, no date_signed widget. The form is filed as the formation sheet inside a transaction bundle (the accompanying Articles of Conversion / Merger / Consolidation), which carries the cover letter, signature, and date. Synth must populate the parent transaction form's cover letter, not this one. Same bundled-sheet pattern as LP_MLPA-12-1 and LLP_MLLP-12-1.
- Open question: filing.accompanying_transaction_type is a new schema-gap key. The 5-way enum mirrors the 5 statutory transaction options visible at the top of page 1; future bundled-formation sheets (e.g., a hypothetical MLLC-6-1 or MNPCA-6-1) may reuse this key family.
- Open question: Text15 and Text16 both map to entity.professional_services_description; this matches the multi-line shape established on the parent MLPA-6 (where Text16+Text17 both fed the same key). Synth concatenates non-empty lines for downstream rubric/text consumers.
