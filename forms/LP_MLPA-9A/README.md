# LP_MLPA-9A — Statement of Withdrawal of a Limited Partner

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** the withdrawing limited partner. If the limited partner is an individual, that person signs the 'Limited Partner*' line and prints their name in Text13. If the limited partner is an entity, an authorized natural person signs the 'For Limited Partner(s) which are Entities' block, identifying the entity in Text14 and their own name+capacity in Text15.

## Purpose

Record the withdrawal of a limited partner from a Maine limited partnership pursuant to 31 MRSA §1346.1.B. The form captures the partnership name, the withdrawing limited partner's name, and a signature block with two parallel paths: an individual-limited-partner block (printed name) and an entity-limited-partner block (entity name + signer printed-name-and-capacity for the natural person signing on the entity's behalf).

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
- Open question: The form provides parallel individual-vs-entity signature paths in line with the per-officer signer pattern (see 2026-04-30-per-officer-signer-pattern.md). Treating the two paths as mutually exclusive at fill time matches LP_MLPA-6's structure for general partners. Confirm by Phase-3 fill that the paths are indeed mutually exclusive in practice.
- Open question: Text11 (legal name of the limited partner) and Text13 (printed signer name) are physically separate widgets. They are typically the same string in practice for individual withdrawals; the schema keeps them distinct so synth and fill preserve form fidelity, but a future helper could populate both from one source.
- Open question: 31 MRSA §1346.1.B governs limited-partner withdrawal. The form does not capture an effective date of withdrawal separate from filing.date_signed; treat them as the same date unless an exhibit is attached.
