# LLC_MLLC-6 — Certificate of Formation (LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 32  
**Mapped fields:** 26  
**Filer role:** authorized person executing the certificate (signs at bottom of page 2)

## Purpose

Form a Maine domestic limited liability company under 31 MRSA §1531, including LLC name, effective date, optional low-profit (L3C) or professional designations, registered-agent designation, and an optional initial statement of authority.

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

- `entity.formation_effective_date_choice` maps to 2 widgets; all receive the same value.
- `registered_agent.type` maps to 2 widgets; all receive the same value.
- `registered_agent.name` feeds two when-gated entries: Text11 when `registered_agent.type = 'commercial'`, Text13 when `'noncommercial'` — only the line matching the selected type is filled.
- `filing.expedited_service` maps to 4 widgets; all receive the same value.
- 1 low-confidence mapping(s) need human review: `filing.expedited_service`
- Open question: The cover-letter expedite section has 4 widgets in the manifest (Check Box14, Check Box15, Check Box16, IMM) but only 3 visible options on the page. Is 'Check Box16' a renamed/orphaned widget left over from an earlier template revision, and should fill logic ignore it?
- Open question: SEVENTH section has an OPTIONAL prefatory checkbox visible on the page but I don't see a corresponding checkbox widget in the manifest — it appears only the inline 'Exhibit __' text field (Text17) was extracted. Is the opt-in checkbox missing from the AcroForm, or merged with the Exhibit field?
- Resolved: the separate 'Name of commercial registered agent' (Text11) and 'Name of noncommercial registered agent' (Text13) lines are when-gated on `registered_agent.type`, so only the row matching the selected type is filled.
