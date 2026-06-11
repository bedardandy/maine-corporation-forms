# CORP_MBCA-20B — Statement of Abandonment of Nonprofit Conversion (Domestic Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 18  
**Mapped fields:** 18  
**Filer role:** officer or other duly authorized representative of the corporation (per the page-0 footnote and 13-C MRSA §936.2)

## Purpose

Abandon a previously filed Articles of Nonprofit Conversion (Form MBCA-20) or Articles of Charter Surrender before the conversion becomes effective, pursuant to 13-C MRSA §936. Filed by a domestic business corporation to halt a pending conversion. The form (2 pages, 18 widgets) captures the entity name (top), the date the original nonprofit conversion was scheduled to become effective (FIRST), the filing date (DATED), the signer's name and capacity (Shape D), plus the standard cover-letter primitive on page 2. Filing fee is $35 per the page-0 header.

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
- Open question: FIRST captures the future effective date of the prior MBCA-20 (Articles of Nonprofit Conversion) filing. Mapped to existing conversion.future_effective_date — semantically the same date, just referenced from the abandonment perspective. An alternative name like conversion.abandoned_effective_date was considered but rejected in favor of reusing the existing key.
- Open question: Form has no widget for the actual signature line — only the typed-name-and-capacity widget. Same convention as MBCA-13A and other Shape-D forms (signature is wet-ink, captured outside the AcroForm).
- Open question: Field-id naming is mixed-case ('20bOne', '20BTwo', '20bThree', '20Bfour') — preserved verbatim. Filler engine must handle both.
- Open question: The form does not capture WHICH prior filing is being abandoned (no exhibit letter for the original Articles of Nonprofit Conversion). Per §936.2, the SOS identifies the prior filing by entity name + filing date. No additional schema key needed.
