# CORP_MBCA-12E-NCRA — Statement of Resignation of Noncommercial Registered Agent (Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 22  
**Filer role:** the noncommercial registered agent who is resigning (signs the lower half of page 0 over the '(signature of noncommercial registered agent)' caption)

## Purpose

File a statement of resignation by the noncommercial registered agent currently appearing on the Maine SOS record for a foreign business corporation, pursuant to 5 MRSA §111. The agent attests to their identity and address as on record, names a person at the corporation to whom the SOS-required notice will be sent, and signs the statement. After filing the agent's appointment terminates 31 days after this statement is delivered to the corporation (per 5 MRSA §111).

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
- Open question: Page 0 has no explicit signature-image widget separate from Text8. Text8 sits below the '(signature of noncommercial registered agent)' caption with its own '(type or print name)' caption, suggesting it captures only the typed/printed name; the actual signature is presumably handwritten or applied as an image after print, not via an AcroForm field. Confirm against fill-engine behavior.
- Open question: The '5 MRSA §111' citation governs noncommercial-RA resignations across all entity types; this form is the foreign-BC variant in a family that likely also includes domestic-BC, LLC, LP, NP variants (look for siblings 12E series). Reviewer should check whether canonical keys here align with those siblings when the rest are processed.
- Open question: The form’s text references the 'foreign business corporation' but the FIRST/SECOND structure is identical to domestic-RA-resignation forms; the only entity-type-specific element is the title block at the top of page 0. Synth's entity-type-specific name suffix logic does not apply here — the entity already exists and its name must match the record exactly.
