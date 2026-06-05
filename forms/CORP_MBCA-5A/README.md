# CORP_MBCA-5A — Termination of Statement of Intention to Do Business Under an Assumed or Fictitious Name (Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 18  
**Mapped fields:** 16  
**Filer role:** any duly authorized officer of the corporation OR the clerk (per 13-C MRSA §121.5 footnote on page 0)

## Purpose

Terminate a previously filed Statement of Intention to do business under an assumed or fictitious name for a Maine domestic business corporation pursuant to 13-C MRSA §404.8. Records the corporation's real name, the assumed/fictitious name being terminated, the signing date, and the signer (any duly authorized officer or the clerk).

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
- Open question: Cover-letter widget naming on this 2003-revision template: 'Check Box1/2/3' (instead of 14/15/16) and 'Name of entitys on the submitted filings 1' (instead of 'Name of entity'). Filler should accept either field-id family. Same upstream-naming-inconsistency note applies as for NP_MNPCA-10 and NP_MNPCA-10A.
- Open question: The original-registration form CORP_MBCA-5 is uninspected in this batch; its mapping for the assumed/fictitious-name widget should use the same canonical key (entity.assumed_or_fictitious_name) so that termination and registration share the concept. Verify when MBCA-5 is reviewed.
- Open question: The signature line on the form ('signature of any duly authorized person') has no separate AcroForm widget — only Text 5aFour ('type or print name and capacity') is bound. Signature is collected as wet-ink/image overlay (consistent with sibling forms).
