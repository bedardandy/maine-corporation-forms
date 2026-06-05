# MARK_mark5 — Class Numbers for Marks (Trademark Reference Guide)

**Entity type:** Trademark / Service Mark  
**Statute:** Maine Trademark Act (10 M.R.S. ch. 301-A)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 0  
**Mapped fields:** 0  
**Filer role:** N/A — reference document, not filed

## Purpose

Reference document listing the 43 Nice Classification classes for goods (1-34) and services (35-43). Distributed alongside MARK_mark1 (registration) to help filers select the correct class number(s) for their mark. Not a fillable form — contains zero AcroForm widgets.

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

- Open question: MARK_mark1 (registration) and MARK_mark4 (assignment) have body-level fields for the class number(s) of the mark; the canonical key for those is currently mark.class_numbers (per MARK_mark1 schema). The class names enumerated in this reference doc (e.g., '009 — Computer software', '041 — Education services') are advisory copy for synth/UI to pick from, not a separate canonical-key namespace.
- Open question: Inclusion convention: this file is committed to maintain 1:1 form_id coverage with sos_forms_inventory.json. Downstream consumers should branch on parsed.is_fillable === false.
