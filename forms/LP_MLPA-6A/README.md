# LP_MLPA-6A — Restated Certificate of Limited Partnership

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 48  
**Mapped fields:** 40  
**Filer role:** all general partners listed in Item Sixth (certificate must be signed by all GPs); entity GPs sign through an authorized representative on page 2

## Purpose

Restate the Certificate of Limited Partnership for an existing Maine domestic limited partnership under 31 MRSA §1322.5. Records the LP's current name (as on file with SOS), any new name, the initial filing date, designated-office address, registered agent (commercial or noncommercial), updated general-partner roster (3 inline rows + exhibit overflow), optional LLLP/professional-LLLP elections, and dual signature blocks for individual GPs (page 1) and entity GPs (page 2).

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

- `registered_agent.type` maps to 2 widgets; all receive the same value.
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `entity.professional_services_description` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Three signature widgets on page 1 — Text22 (rect [35.5,173.3,288.6,193.9]), Text25 ([35.5,139.7,288.6,160.3]), Text27 ([36.5,107.1,289.5,127.7]) — are intentionally omitted from field_mappings: they are the left-column '(signature)' lines for GP rows 1-3, which are wet-ink-only per the MLPA-6 sibling convention. Synth fixtures should leave them blank; the filler does not populate signature widgets.
- Open question: Template gap on page 1: the inline 'Exhibit ___' letter blank next to Check Box18 ('Names and addresses of additional general partners are attached as Exhibit ___') is visible on the page but missing from the AcroForm. Filer must write the exhibit letter by hand. Recommend upstream fix.
- Open question: Template gap on page 1: the NINTH paragraph contains an inline 'Exhibit ___' blank ('Other provisions...are set forth in the attached Exhibit ___') that is also missing from the AcroForm. Text30 (the only candidate small-width blank in this page region) is the 'Dated ___' line, not the NINTH exhibit blank. Recommend upstream fix.
- Open question: Template gap on page 0: THIRD section visually shows two underlines (physical-address line + mailing-address line) but widgets.json contains only ONE widget (Text4) for THIRD. The mailing-address line of the designated office has no AcroForm widget. Mapping uses Text4 → entity.designated_office.physical_address; filer must write designated-office mailing address by hand if different from physical.
- Open question: Page-0 Restated-cert specific: the FIRST (new name), SECOND (initial filing date), and THIRD (designated office) clauses are unique to a Restated Certificate and do not appear on MLPA-6 (the original certificate). Cross-check that filler/synth handles the entity.name → entity.new_name distinction correctly: entity.name = name as on record; entity.new_name = post-restatement name (may be unchanged).
