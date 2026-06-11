# NP_MNPCA-6-1 — Articles of Incorporation (Nonprofit) — to accompany Conversion or Restatement

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 23  
**Mapped fields:** 17  
**Filer role:** n/a on this attachment — the primary form (Conversion or Restatement) carries the filer/signer block. This form supplies only the substantive articles content.

## Purpose

Attachment-form variant of MNPCA-6 (Articles of Incorporation, 13-B MRSA §403) used when articles are filed alongside an Articles of Nonprofit Conversion (13-C MRSA §933), Statement of Conversion (31 MRSA §1645), or Restated Articles of Incorporation (13-B MRSA §805). Captures entity name, public-vs-mutual benefit purpose, registered agent, board structure, member structure, and optional 501(c)/political-activities provisions. Has no incorporator signature block — signatures are on the accompanying primary document and no cover-letter block (cover letter is filed with the primary).

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

- `filing.accompanying_document_type` binds as a single enum_select selecting among 3 option widgets (accepted values: articles_of_nonprofit_conversion, statement_of_conversion, restated_articles_of_incorporation).
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `entity.has_members` binds as a single enum_select selecting among 2 option widgets (accepted values: True, true, yes, False, false, no).
- Open question: This attachment-form variant lacks both the incorporator signature block (page 1 of MNPCA-6) AND the cover-letter block (page 3 of MNPCA-6). Both are presumed to live on the accompanying primary form (Conversion / Restatement). When synth/rubric runs against MNPCA-6-1, those keys should NOT be required here.
- Open question: MNPCA-6 uses parallel widget mechanisms for SEVENTH/EIGHTH (X-mark text widgets PLUS AcroForm checkboxes). MNPCA-6-1 uses ONLY AcroForm checkboxes (Check Box16, Check Box17) — cleaner. Should fill engine prefer this template's checkbox-only design for future template revisions of MNPCA-6?
- Open question: FIFTH layout: Text27 is on the right side of the min/max line (y=703) and Text28 is on the left side of the next visual row (y=682). This mirrors NP_MNPCA-6's Text14 (right) / Text15 (left) where min sits on the right of the wrapped sentence and max wraps to the left — confirmed via rect comparison with NP_MNPCA-6.
