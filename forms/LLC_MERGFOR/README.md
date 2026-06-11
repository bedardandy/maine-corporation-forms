# LLC_MERGFOR — Merger (Foreign Entities)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 21  
**Filer role:** Authorized representative of the foreign entities. The form has no AcroForm signature widget on the body — the certified-copy attachment from the home jurisdiction supplies the signature/authorization.

## Purpose

File with the Maine SOS a merger involving foreign entities where at least one party is qualified or registered in Maine. Records the surviving foreign entity's home name, jurisdiction, Maine-authorization date, and any post-merger name change; and the nonsurviving foreign entity's home name, jurisdiction, and Maine-authorization date. A certified copy of the merger (or certificate of merger) from the home jurisdiction must be attached. The page-1 fee table sets filing fees by entity type ($25 foreign nonprofit; $100 foreign business corporation; $150 foreign LP per 31 MRSA §1411 / foreign LLP per 31 MRSA §1438).

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
- Open question: This LLC-namespaced template uses sequential widget names (Text1..Text21, Check Box10..Check Box12) on the cover-letter page where the corp-namespaced sibling CORP_MERGFOR.pdf uses descriptive names ('Name of contact person', 'Check Box14', etc). Body and cover-letter mappings to canonical keys are identical between the two; only widget IDs differ. The filler engine binds by widget ID, so both templates must be tracked separately even though they represent the same form.
- Open question: Form has no AcroForm signature widget on the body — authorization is supplied by the certified copy from the home jurisdiction. Synth fills can leave the body unsigned.
- Open question: Only one inline slot for the nonsurviving entity. Multi-entity mergers (>1 nonsurviving) attach additional pages — the schema does not currently capture an exhibit-letter or list shape for them.
- Open question: Considered using merger.parties[N].* (per MBCA-10) instead of split surviving_entity / nonsurviving_entity. Chose the survivor/nonsurvivor split to mirror the form's literal recitals — MBCA-10's parties[N] list is more flexible but the FIRST/SECOND structure of this form binds tightly to the two named roles.
