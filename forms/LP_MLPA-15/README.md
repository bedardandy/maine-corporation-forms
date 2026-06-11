# LP_MLPA-15 — Application for the Use of an Indistinguishable Name

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** at least one general partner of the consenting LP listed on the certificate of limited partnership (per footnote ** citing 31 MRSA §1324.1.J). Only one signature slot is provided on this form (compare MLLC-15 which has two).

## Purpose

A Maine limited partnership consents to another entity's use of an indistinguishable name pursuant to 31 MRSA §1308.D.1. The consenting LP undertakes to change its own name to one that is distinguishable on SOS records, and the application MUST be accompanied by the corresponding name-change filing (e.g., LP_MLPA-9 Certificate of Amendment).

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
- Open question: Per footnote *, this form MUST be accompanied by a name-change filing. For an LP that's typically LP_MLPA-9 (Certificate of Amendment). At assemble time, synth must bundle MLPA-15 with the matching MLPA-9 and propagate name_consent.replacement_name into the bundled form. Confirm the bundling form-id mapping (LP→MLPA-9, LLC→MLLC-9).
- Open question: Statute citation differs from MLLC-15: MLPA-15 cites §1308.D.1 (LP-suffix availability) while MLLC-15 cites §1508.4 (LLC-suffix availability). Both fall under the broader name-availability framework but are housed under different titles (31 MRSA Ch. 17 for LP, Ch. 21 for LLC). No schema impact, but note the parallel.
- Open question: Single-signer pattern (Shape D, filing.signer.*) — contrast with MLLC-15's filing.signer_N.* multi-signer pattern. The two sister forms differ in how many authorized signers they contemplate; both are correct per their respective statutes (§1324.1.J vs §1676.1B).
- Open question: The schema_gaps list is empty for this form because all introduced keys (name_consent.*) are inherited from MLLC-15's pass-1 — once that JSON is committed first, MLPA-15 is purely a reuse of those keys plus the cover-letter primitive. If MLPA-15 is committed first, the name_consent.* gaps move here instead.
