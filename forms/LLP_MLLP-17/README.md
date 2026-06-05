# LLP_MLLP-17 — Certificate of Correction (Domestic Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 22  
**Mapped fields:** 20  
**Filer role:** partner OR duly authorized person OR a partner-entity's authorized signer (signs on page 1)

## Purpose

Correct an inaccurate or defectively-executed previously-filed document for a Maine domestic Limited Liability Partnership under 31 MRSA §824. Identifies the original filing date, describes the inaccuracy/defect, and supplies the corrected text. Per 31 MRSA §826.1.B/2 the certificate must be signed by at least one partner OR by a duly authorized person; an entity-partner alternative signature block is provided.

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
- Open question: Template-level upstream bug: FIRST has TWO blanks visible on the rendered page — the date blank (Text2 widget) and the 'partnership entitled' document-type blank (NO widget). Only 4 widgets exist on page 0 (Text1=name, Text2=date, Text3=defect, Text4=corrected text), leaving the document-type blank unbindable. Cannot be filled at fill time without an upstream `normalize_fields` pass — same class of issue as MNPCA-10 missing FIRST checkboxes (Phase-2 summary). Tracked: correction.original_document_type schema gap is reserved but unbound on this form.
- Open question: filing.signer_entity.* introduces a new namespace family — analogous to per-officer-signer-pattern's `<role>_entity_N.*` but unindexed and rooted at filing.signer.* rather than at a role key. This makes sense because MLLP-17 is not a formation form (no role-keyed originators); the filer is the entity itself, with one signer slot that may be either a natural-person partner or an entity-partner-with-natural-signer. If a future correction-style form has multiple entity-partner signers, the namespace should be indexed (filing.signer_entity_N.*).
- Open question: Drafter's mapping originally swapped Text3 (large box) → 'partnership entitled' and Text4 (large box) → defect description. The rect heights (~118pt and ~114pt) make the swap clear: both are multi-line text boxes, not single-line widgets. Fixed in this review.
