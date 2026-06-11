# LLP_MLLP-17A — Certificate of Correction (Foreign Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 24  
**Mapped fields:** 24  
**Filer role:** partner OR duly authorized person OR an entity-partner's authorized signer (signs on page 1)

## Purpose

Correct an inaccurate or defectively-executed previously-filed document for a foreign Limited Liability Partnership authorized to do business in Maine, pursuant to 31 MRSA §856. The form identifies the foreign LLP, its home jurisdiction, the date and title of the original document, the inaccuracy or defect, and the corrected text. Two parallel signature blocks are provided on page 1 — one for an individual partner / duly authorized person and one for an entity-partner with its natural-person signer.

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
- Open question: Both signature blocks (individual partner / entity partner) on page 1 expose only the printed-name-and-capacity widget; the (signature) and (authorized signature) lines above them are wet-ink-only with no AcroForm widget — consistent with LLP_MLLP-17 and other Shape-D forms.
- Open question: Form is governed by 31 MRSA §856 (LLP correction). The foreign-LLP variant differs from LLP_MLLP-17 (domestic) only in (a) using entity.home_jurisdiction_name + entity.home_jurisdiction instead of entity.name and (b) having a bound widget for correction.original_document_type that the domestic template lacks.
- Open question: Filer-role footnote allows either a partner or 'a duly authorized person'. The signer's role label entered in the printed_name_and_capacity widget should reflect this (no enum needed).
