# NP_MNPCA-19A — Statement of Abandonment of Domestication and Conversion (Foreign Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 17  
**Mapped fields:** 17  
**Filer role:** an officer or other duly authorized representative of the foreign nonprofit corporation (signs the *By line at the bottom of page 0; widget captures '(type or print name and capacity)')

## Purpose

Abandon a previously-filed domestication and conversion of a foreign nonprofit corporation in Maine. The corporation recites (FIRST) that the abandonment was effected in accordance with the laws of its foreign jurisdiction after the original articles of domestication and conversion were filed with the Maine SOS, and (SECOND) that this statement takes effect upon filing such that the domestication and conversion is considered abandoned and does not become effective. Only 3 body widgets: entity name, dated, signer. Filing fee $35 per page-0 header.

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
- Open question: Form recites 'Pursuant to 13-C MRSA §944' but the page-0 heading is FOREIGN NONPROFIT CORPORATION — 13-C is the Maine Business Corporation Act; nonprofit corporations are governed by 13-B MRSA. Likely an upstream template-text error (template was probably forked from the BC abandonment form CORP_MBCA-19? and not updated). The 13-B equivalent statute for abandonment of domestication and conversion would need to be confirmed (possibly 13-B §1414 or a parallel section). Does not affect canonical-key mapping — flagged for upstream attention.
- Open question: Body has only 3 fillable widgets (entity name, dated, signer); FIRST and SECOND paragraphs are pure recitals with no widgets. This is a 'recitation-only' form similar to CORP_MBCA-19A's structure — the legal effect comes from signing the recitations, not from filling additional fields.
- Open question: *By signature line above 19aThree has no corresponding AcroForm widget — the actual signature is applied as wet-ink/image overlay after print. Same template convention as CORP_MBCA-19A and most 13-C/13-B body forms.
- Open question: Form does not capture which prior filing is being abandoned (e.g., the original articles-of-domestication-and-conversion filing's effective date or filing receipt number). The SOS presumably matches by entity name plus by being a unique pending domestication. Not a canonical-key issue, but noteworthy: a strict abandonment-rubric cross-check would require an out-of-band reference to the original filing record.
