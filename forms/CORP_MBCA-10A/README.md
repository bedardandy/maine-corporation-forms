# CORP_MBCA-10A — Statement of Abandonment of Merger or Share Exchange

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 21  
**Filer role:** officer or other duly authorized representative of one party to the merger or share exchange (per the form's footnote: '*This document MUST be signed by an officer or other duly authorized representative of a party to the merger or share exchange'). Single signer regardless of how many parties were originally to the merger.

## Purpose

Abandon a previously filed Articles of Merger or Share Exchange (MBCA-10) before it becomes effective, pursuant to 13-C MRSA §1108.2. The form identifies the party filing the abandonment, lists up to four parties to the original transaction, and is signed by a single authorized representative (Shape D — combined name+capacity).

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
- Open question: SECOND has 4 inline party rows (10a2-10a5). The form text says 'attach additional pages if necessary' is NOT present here (unlike MBCA-10). If a merger has >4 parties, the abandonment statement may be missing an exhibit affordance — confirm whether SOS accepts handwritten attachments.
- Open question: 13-C §1108.2 requires that the abandonment occur 'before the effective time' and be filed by 'each constituent party' or 'one or more parties as the plan provided'. Form is signed by only one party — implying only that one party need file the abandonment, but the recital lists all parties. Synth should populate all known merger parties even though only the filer signs.
- Open question: The THIRD recital ('This statement takes effect upon filing, and the merger or share exchange is considered abandoned and does not become effective.') is fixed boilerplate with no widgets — no canonical key needed.
- Open question: Considered using merger.parties[N].name (split from jurisdiction/type) since the columns are visually separated. Chose merger.parties[N].recital to match MBCA-10's combined-recital convention, since the underlying widget is single per row regardless of how many column headers are printed.
