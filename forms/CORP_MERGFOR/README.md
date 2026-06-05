# CORP_MERGFOR — Merger (Foreign Entities)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** Authorized representative of the foreign entities. The form has no AcroForm signature widget on the body — the certified-copy attachment from the home jurisdiction supplies the signature/authorization.

## Purpose

Record with the Maine SOS a merger involving foreign entities where at least one party is qualified or registered in Maine. The form captures the surviving foreign entity's home name, jurisdiction, Maine-authorization date, and any post-merger name change; and the nonsurviving foreign entity's home name, jurisdiction, and Maine-authorization date. A certified copy of the merger (or certificate of merger) from the home jurisdiction must be attached. Per the page-1 fee table the filing fee depends on the entity type ($25 for foreign nonprofit; $100 for foreign business corporation; $150 for foreign LP/foreign LLP under 31 MRSA §1411 / §1438).

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
- Open question: Form has no AcroForm signature widget on the body — authorization is supplied by the certified copy from the home jurisdiction. Synth fills can leave the body unsigned.
- Open question: Only one inline slot for the nonsurviving entity. Multi-entity mergers (>1 nonsurviving) attach additional pages — the schema does not currently capture an exhibit-letter or list shape for them.
- Open question: The form title 'Merger (Foreign Entities)' and the 'Surviving Foreign Entity' / 'Nonsurviving Foreign Entity' singular labels imply both parties are foreign. A domestic-into-foreign merger likely uses a different form (or the domestic-merger MBCA-10 with foreign-survivor election). Out of scope for this pass-1.
- Open question: Considered using merger.parties[N].* (per MBCA-10) instead of split surviving_entity / nonsurviving_entity. Chose the survivor/nonsurvivor split to mirror the form's literal recitals — MBCA-10's parties[N] list is more flexible but the FIRST/SECOND structure of this form binds tightly to the two named roles.
