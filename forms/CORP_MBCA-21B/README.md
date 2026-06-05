# CORP_MBCA-21B — Articles of Charter Surrender (Upon Entity Conversion)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** an officer or other duly authorized representative of the corporation per 13-C MRSA §956.1 (signs at bottom of page 0)

## Purpose

Surrender the charter of a Maine domestic business corporation that has converted into a foreign unincorporated entity (LLC, LP, GP, or other non-Maine non-corporate form) under 13-C MRSA §§956 and 957. Records the effective date of the conversion, the jurisdiction of the surviving entity, the address of the surviving entity's executive office (required only if the surviving entity is a nonfiling entity), and the mailing address at which the Secretary of State will be served any process relating to shareholder appraisal rights under chapter 13 of Title 13-C. Filing fee is $90.

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
- Open question: FOURTH paragraph asks for executive-office address only 'If the surviving entity is a nonfiling entity'. There is no checkbox to indicate filing vs nonfiling status, so the rubric must infer it from conversion.surviving_entity_jurisdiction plus an inferred surviving-entity type — the form does not capture the latter. A future schema-gap key conversion.surviving_entity_type (LLC/LP/GP/etc.) would let the rubric branch deterministically.
- Open question: SECOND paragraph recites that the conversion was duly approved by the shareholders but has no widget — approval is implicit in the filing. Same pattern as MBCA-21's THIRD paragraph. No rubric check needed beyond the form-level signature.
- Open question: SIXTH paragraph recites an undertaking to pay shareholders any amount they are entitled to under chapter 13, with no widget — implicit obligation, no rubric check.
- Open question: Cover-letter filing.entities[1].name has no obvious counterpart on this filing (charter surrender is single-entity; no bundled formation form like MBCA-21's MLLC-6/MLPA-6 attachment). Likely left blank in practice; same generic SOS cover-letter primitive as elsewhere.
