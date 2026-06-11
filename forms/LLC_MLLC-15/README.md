# LLC_MLLC-15 — Application for the Use of an Indistinguishable Name

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 21  
**Filer role:** person authorized by the consenting LLC (per footnote ** citing 31 MRSA §1676.1B). Form provides two parallel signer slots for cases where bylaws/operating agreement require dual signatures.

## Purpose

A Maine LLC consents to another entity's use of an indistinguishable name pursuant to 31 MRSA §1508.4. The consenting LLC undertakes to change its own name to one that is distinguishable on SOS records, and the application MUST be accompanied by the corresponding name-change filing (e.g., MLLC-9 Articles of Amendment).

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
- Open question: Per footnote *, this form MUST be accompanied by a name-change filing (typically MLLC-9 Articles of Amendment for the consenting LLC). At assemble time, synth must bundle MLLC-15 with the matching MLLC-9 and set amendment.new_name consistently across both. Should `filing.bundled_forms[]` be added as a generic schema gap to track these required attachments?
- Open question: Two signer slots exist on the form but the statute (§1676.1B) requires only one signer. Synth should populate signer_1 always and signer_2 only when an operating agreement requires dual authorization. Rubric currently requires signer_1 only — confirm this matches how SOS evaluates incoming filings.
- Open question: The 'name_consent.requestor.*' sub-namespace is introduced for the requestor's name only — no requestor address or jurisdiction widget exists on this form. If a future form variant adds those, they would extend the same sub-namespace.
- Open question: There are no AcroForm widgets for the two signature lines themselves (just the printed-name-and-capacity widgets). Signatures are intended to be wet-ink; consistent with other Maine SOS forms.
