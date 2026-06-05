# CORP_SOPAPPT — Statement of Appointment of Agent for Service of Process for a Nonfiling Domestic Entity or a Nonqualified Foreign Entity

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** duly authorized officer of the entity (signs at bottom of page 0). Per the * footnote: 'This statement MUST be signed by any duly authorized officer.'

## Purpose

Appoint an agent for service of process for a nonfiling domestic entity (e.g., general partnership, sole proprietorship, trust, unincorporated association — entities not required to file formation documents with SOS) or a nonqualified foreign entity transacting business in Maine, under 5 MRSA §112. The appointment is effective for 5 years from filing. Captures the entity's legal name and free-text type, jurisdiction of organization, and the agent's name and physical address (P.O. Box explicitly prohibited). Filing fee $100. Distinct from the registered_agent.* and clerk.* patterns used by formation/qualification forms — this form has neither because the appointing entity is neither registered nor qualified.

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
- Open question: FIFTH paragraph ('This statement appointing an agent for service of process is effective for a period of 5 years after the date of filing') is a fixed statutory recital with no widgets — it doesn't require filer input but is the substantive operative effect of the filing.
- Open question: entity.type is free-text. A future cleanup pass could enumerate the canonical values ('General Partnership', 'Sole Proprietorship', 'Trust', 'Unincorporated Association', 'Other domestic nonfiling entity', 'Foreign nonqualified entity') to enable rubric/synth round-tripping. Left as free-text for now to match the form's open prompt.
- Open question: agent.* is a new namespace, deliberately separate from registered_agent.* and clerk.*. If a future §112-style appointment surfaces (e.g., for a different statute), the agent.* namespace can host it. If no other §112 forms emerge, this namespace stays single-form.
- Open question: Page-0 layout is unusually compact: all 7 body widgets and the cover letter spans 2 pages total (most SOS forms are 3+ pages). Filer_role inferred from the * footnote — no separate authority-tier rule like LLP §825's three tiers.
