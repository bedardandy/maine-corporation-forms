# CORP_MBCA-11A — Articles of Revocation of Dissolution

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 23  
**Mapped fields:** 18  
**Filer role:** any duly authorized officer OR the clerk (per 13-C MRSA §121.5)

## Purpose

Revoke a previously filed dissolution of a Maine domestic business corporation under 13-C MRSA §1405. Records the effective date of the original dissolution being revoked, the date the revocation was authorized, the body that authorized the revocation (incorporators / board / board with prior shareholder authorization / shareholders), and the signature of any duly authorized officer or clerk.

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

- `revocation.authority_type` maps to 4 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: The (signature) line on page 0 has no AcroForm widget — only widget 11a9 captures the printed name+capacity. Wet-ink signature expected at fill time, similar to MBCA-11 dissolution.
- Open question: Form does not capture which BODY originally authorized the dissolution (only who is now revoking it). The 'board_with_shareholder_authorization' Box6 implicitly references that the prior dissolution was shareholder-approved, but the schema does not record the original authorization mode.
