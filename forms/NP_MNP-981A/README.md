# NP_MNP-981A — Certificate of Organization (Domestic Nonprofit Corporation, 13 MRSA §981-A)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 50  
**Mapped fields:** 45  
**Filer role:** two officers of the existing nonprofit corporation: the President and the Secretary/Clerk (per the page-2 signature block, which provides exactly two signature slots labeled (President) and (Secretary/Clerk) — fixed, not variable).

## Purpose

File a Certificate of Organization for an existing Maine domestic nonprofit corporation under 13 MRSA §981-A. The undersigned officers recite the corporation's original organization details (place, date, original name), historical name changes (up to 5 inline rows), original purposes, current public/mutual benefit classification, current management structure (directors vs members), current located-at address, and full officer roster. Unlike a NPCA-6 formation filing, the corporation already exists; this is a §981-A re-recital filing. Distinct from the modern NPCA-6 incorporator pattern — signers are sitting officers (President and Secretary/Clerk).

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

- `entity.original_name` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: FOURTH original-name has two widget lines (981a17 short, 981a18 wider continuation). Both bind entity.original_name. Synth/filler must split a long name across the two; short names should leave 981a18 empty. Open whether to introduce a `entity.original_name_line2` convention or rely on a line-wrap helper.
- Open question: Page-2 signature block: each (President) and (Secretary/Clerk) row has two horizontal lines — one for wet-ink signature and one labeled '(type or print name)'. Only the printed-name line has an AcroForm widget (981a35, 981a36). Signature lines are not bindable.
- Open question: EIGHTH includes a county widget (981a28) — atypical for Maine SOS address blocks, which usually omit county. This is specific to the §981-A recital text and should not be generalized to other forms' entity.current_address.* keys.
- Open question: SIXTH mutual-benefit text reads 'organized as a mutual benefit corporation for all purposes permitted under 13-B MRSA, or, if not for all such purposes, then for the following purpose or purposes'. This means an empty entity.mutual_benefit_purpose is valid (covers 'all purposes permitted'); a non-empty value narrows the scope. Rubric reflects this conditional.
- Open question: filing.signer_<role> pattern is new (proposed in schema_gaps). It mirrors the existing officer_<role> roster convention but applies to signature slots. Future per-role signature forms should follow this pattern rather than introducing yet another shape.
