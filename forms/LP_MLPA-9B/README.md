# LP_MLPA-9B — Statement of Dissociation (Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** the dissociating general partner (individual GP signs in own name; entity GP signs through an authorized representative)

## Purpose

File a standalone Statement of Dissociation by a general partner of a Maine limited partnership pursuant to 31 MRSA §1375.1.D. The form names the LP and the dissociating GP, and is signed by that GP (per footnote: 'Certificate MUST be signed by the person dissociated as a general partner. (31 MRSA §1324.1.G)'). The signer is therefore identical to the dissociated GP — individual or entity.

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
- Open question: The form has no explicit checkbox to elect the individual-vs-entity signature path. Pass-1 leaves selection implicit (whichever signer block is populated). Synth must populate exactly one path; rubric should treat populating both as an error.
- Open question: Item 31 MRSA §1375.1.D is the substantive ground for filing; §1324.1.G governs WHO must sign. No form fields capture additional notice to other partners or creditors — that is an off-form statutory obligation, not a schema concern.
