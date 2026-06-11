# CORP_MBCA-10 — Articles of Merger or Share Exchange (Survivor is a Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 42  
**Mapped fields:** 45  
**Filer role:** an officer or other duly authorized representative of each participating party signs in the per-party signature block on page 2 (per 13-C MRSA §1106.8)

## Purpose

File Articles of Merger or Share Exchange under 13-C MRSA §1106 when the surviving/acquiring entity is a Maine business corporation. Records the multi-party recital, surviving entity, principal place of business, exhibit attachments for amendments or new-corporation provisions, future effective date, shareholder/foreign-authorization elections, foreign survivor service-of-process address, and per-party signature blocks (up to 3 inline + copy-page overflow).

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

- `merger.fourth_election.*` maps to 2 independent boolean checkboxes (survivor_originating_doc_amended, new_corporation_created).
- `merger.sixth_election.*` maps to 2 independent boolean checkboxes (shareholder_approval_obtained, shareholder_approval_not_required).
- `merger.seventh_election.*` maps to 2 independent boolean checkboxes (foreign_corp_authorized, eligible_entity_authorized).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: Three /Btn widgets on page 1 (rects y≈551, y≈514, y≈463) and three /Btn widgets on page 3 (cover-letter expedite tiers) have empty /T (no field name) per pypdf. The form-fill engine binds checkboxes by /T elsewhere — these unnamed widgets likely need positional binding or a normalize pass to assign names. This is a template-level upstream bug (compare to MLLC-12 SIXTH commercial/noncommercial which had Check Box15/16 page-null but at least had names). Confirm with pdftk dump_data_fields once installed.
- Open question: FIRST recital block has 4 inline rows but page-2 signature block has only 3 inline party slots. Form's inline note says 'Copy this page, and modify participant number, if more signature spaces are needed' — confirm: parties[3].recital + parties[N≥3].signature_block live on attached copies of page 2.
- Open question: SECOND surviving-entity widget Text7 combines name+jurisdiction in one field (header has two columns 'Name | Jurisdiction' but only one underlined blank). Parser should split on whitespace + jurisdiction-token heuristic, or accept combined value at fill time.
- Open question: FIFTH future_effective_date is unbounded — filers can set arbitrarily-far future dates. Title 13-C §107 may impose limits (e.g., 90 days or a fiscal-year boundary); confirm whether rubric should enforce an upper bound.
- Open question: FOURTH option 2 references 'attached MBCA-6-1' (Articles of Incorporation to be attached to merger/conversion docs). This is an inter-form reference — when fourth_election='new_corporation_created' and the new corp is domestic, an MBCA-6-1 filing is bundled. Cross-form filing.bundled_forms[] tracking is not yet a canonical key family.
