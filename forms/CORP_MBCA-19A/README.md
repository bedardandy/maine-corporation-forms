# CORP_MBCA-19A — Articles of Charter Surrender (Upon Domestication)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** an officer or other duly authorized representative of the corporation per 13-C §924.1 (signs the *By line at the bottom of page 0; widget captures '(type or print name and capacity)')

## Purpose

Surrender the Maine charter of a domestic business corporation in connection with its domestication into a foreign jurisdiction under 13-C MRSA §§924–925. Records the effective date of domestication, the new home jurisdiction, the corporation's appointment of the Secretary of State as agent for service of process for shareholder-appraisal-rights enforcement, and a mailing address to which the SOS will forward such process. Filing fee $90 (per page 0 header).

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
- Open question: Page 0 widget IDs use the '19aN' naming pattern (form-id-prefixed) instead of generic 'TextN' / numbered widgets seen on other 13-C forms. Likely a template authoring convention; confirm fill-engine handles both schemes uniformly.
- Open question: The *By signature line above 19a6 has no corresponding AcroForm widget on this form (template gap — page 0 has only 6 widgets total, all text). The actual signature is applied post-print as a handwritten/image signature.
- Open question: SECOND and FIFTH paragraphs are pure recitations (shareholder-approval and pay-appraisal-amount obligations) — no fillable widgets, only legal commitments restated by signing the form. No canonical keys needed for these recitals.
- Open question: 13-C §925 requires a contemporaneous foreign-jurisdiction filing to effect the domestication; this form alone is incomplete. Filing-orchestration logic should coordinate the Maine surrender with the foreign filing, but that is out of scope for the SOS pass-1 schema.
