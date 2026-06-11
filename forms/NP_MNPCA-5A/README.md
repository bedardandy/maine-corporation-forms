# NP_MNPCA-5A — Termination of Statement of Intention to Carry on Activities Under an Assumed or Fictitious Name (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 21  
**Filer role:** duly authorized officer of the nonprofit corporation per 13-B MRSA §104.1.B (two signature blocks provided; both expected to be signed)

## Purpose

Terminate a previously filed Statement of Intention to Carry on Activities Under an Assumed or Fictitious Name (NP_MNPCA-5) for a Maine domestic nonprofit corporation under 13-B MRSA §308-A.8. Records the corporation's real (legal) name, the specific assumed/fictitious name being terminated, the Maine registered office address, and dual signatures by authorized officers. Filing fee is $5.

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
- Open question: FIRST paragraph ('The corporation no longer intends to carry on activities under an assumed or fictitious name.') is recital text with no widget — implicit in the filing.
- Open question: Drafter originally proposed entity.fictitious_name_terminated as a new schema_gap; reviewer collapsed onto the existing assumed_name.name key (used by CORP_ASUM-5 / CORP_FICT-4 family) since the form treats 'assumed' and 'fictitious' as synonymous in the §308-A.8 nonprofit termination context. No new schema_gap is required — all keys on this form already exist upstream.
- Open question: Form provides two signer slots (Widgets 6 and 7). 13-B MRSA §104.1.B requires only one duly authorized officer to sign, but the form's pre-printed dual-block layout suggests historical practice expected two signers (likely paralleling the corporate-officer signer pairs on older 13-B forms). Synth should populate both for realism; rubric treats the second as optional.
