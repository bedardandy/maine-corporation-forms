# LLP_MLLP-15 — Application for the Use of an Indistinguishable Name (LLP)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** any partner of the existing LLP per 31 MRSA §826.1.B and §860.1 (signs in the bottom signature block on page 0; the form footnote states 'this certificate MUST be signed by at least one partner').

## Purpose

An existing Maine LLP that holds a name now wanted by another applicant uses this form (per 31 MRSA §803-A.4 / §860.1) to (a) consent to the requestor's use of the indistinguishable name and (b) commit to changing its own name to a new, distinguishable name. The form must be accompanied by the applicable name-change form for the existing LLP (FIRST/THIRD references item Third).

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
- Open question: Item 'Third' references a companion name-change form for the LLP. The corresponding LLP name-change filing in this corpus is likely MLLP-11R or another LLP amendment form — not enumerated as a canonical key on this form, but synth/rubric should flag that a companion filing is expected.
- Open question: name_change.* is introduced here as a small new namespace shared with a future indistinguishable-name family (CORP, LLC, NP variants likely exist). If those forms appear later, they should reuse name_change.indistinguishable_name / requestor_name / new_name verbatim.
