# CORP_MBCA-19 — Articles of Domestication (Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 22  
**Filer role:** an officer or other duly authorized representative of the foreign corporation per 13-C MRSA §923 (signs at bottom of page 1)

## Purpose

Domesticate a foreign business corporation into a Maine domestic business corporation under 13-C MRSA §923. Records the corporation's foreign legal name, optional new Maine name (when the foreign name is unavailable or the corporation chooses to change), home jurisdiction and date of original incorporation, the attached Articles of Incorporation exhibit (Form MBCA-6-1), an optional future effective date, and the authorized signer.

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
- Open question: Form requires attached Form MBCA-6-1 (Articles of Incorporation). filing.entities[1].name on the cover letter is likely populated with the bundled-form entity for SOS routing. Same cross-form bundling pattern as MBCA-21 (MLLC-6 / MLPA-6) and MLLC-12 (FICT-4) — a canonical `filing.bundled_forms[]` family is not yet defined; deferred until the pattern is observed on more forms.
- Open question: SECOND paragraph (authorization recital — 'duly authorized as required by the laws of the jurisdiction in which the corporation was incorporated') has no widget and no opt-in checkbox; implicitly affirmed by the act of filing. No rubric check needed beyond the form-level signature.
- Open question: Widget IDs '191'..'198' use digit-only naming (no Text prefix) — same upstream template quirk as MNPCA-10. Filler engine should accept both styles; preserved verbatim in field_id.
- Open question: On a domestication, the corporation's pre-filing identity uses entity.home_jurisdiction_name (foreign legal name) and post-filing it uses domestication.maine_name (or, if unset, the same as home_jurisdiction_name). Consider whether `entity.name` should be auto-derived from these for downstream consistency, or whether MBCA-19 should explicitly omit `entity.name` since it's not a body widget.
