# CORP_HO-E911 — Notification of Change in Home Office Address by Municipality or U.S. Postal Service

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 24  
**Mapped fields:** 23  
**Filer role:** municipal official or postmaster (per footnote 2, the document MUST be signed by the municipal official or postmaster who imposed the change — not by the entity itself)

## Purpose

Notify the Maine Secretary of State of a change in a foreign entity's home-office address caused by a municipality or U.S. Postal Service action (e.g., E-911 street renumbering or USPS-imposed mailing-address change). Filed by a foreign business corporation, LLC, LP, or LLP that has been authorized to transact business in Maine.

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

- `filing.authorized_by` binds as a single enum_text_select selecting among 2 option widgets (accepted values: town_municipality, us_postal_service).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: FOURTH section's two choices (Town/Municipality, U.S. Postal Service) are visually checkboxes but encoded upstream as /Tx widgets (Text7, Text8) rather than /Btn. Filler engine must treat them as mark-with-X-style text widgets, not booleans. Worth a normalize_fields pass to convert to /Btn or to alias the /Tx pair to a single boolean enum.
- Open question: No AcroForm widget for the **By (signature) line — only printed-name-and-capacity (Text10) is captured. The signature is intended to be wet-ink only. Consistent with other SOS forms that omit signature widgets.
- Open question: Header box reads 'No Filing Fee' for HO-E911 but the cover-letter still shows 'Total fee(s) enclosed' and three expedite checkboxes. Confirm whether the expedite tiers actually apply to a no-fee filing or whether they're vestigial cover-letter copy.
