# LLC_MLLCCONV — Statement of Conversion (Maine LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 33  
**Mapped fields:** 30  
**Filer role:** the converting organization (signs page 1 'Must Be Completed by the Converting Organization' block) — two parallel signer slots for combined name+capacity. The form does not specify the role beyond 'authorized representative'; convention is an officer/manager/authorized person of the converting entity per its organic law.

## Purpose

Record with the Maine SOS that an organization has converted into another organization under 31 MRSA §1647 (Maine LLC chapter conversion provisions). Captures parallel identification of the converting (predecessor) and converted/resulting organizations — name, form, jurisdiction, date of organization — plus the resulting entity's principal-office address, the conversion's effective date, a foreign-resulting-entity service-of-process address (when the resulting entity is foreign), and a SEVENTH-recital select-one indicating either the resulting entity's organizing document is attached as an exhibit OR the resulting entity is not a Maine SOS filer.

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

- `conversion.organizing_document_disposition` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Reviewer restructured the namespace from drafter's parallel conversion.converting_entity.* / conversion.resulting_entity.* (which would conflict with the existing convention from MBCA-21 / GP_CONV-PARTNER) to entity.* (converting/predecessor) + conversion.new_entity.* (resulting) — matching the established post-conversion namespace and reusing existing keys (entity.name, entity.home_jurisdiction, entity.original_articles_filing_date, conversion.new_entity.name, conversion.new_entity.type, conversion.new_entity_provisions_exhibit_letter).
- Open question: Page-1 has TWO 'type or print name and capacity' widgets (Text 'type or print name and capacity' + Text 'type or print name and capacity_2'). Drafter mapped the first to filing.signer.printed_name_and_capacity and the second to filing.signer_2.* — reviewer corrected to filing.signer_1.* / filing.signer_2.* for multi-slot consistency with MLLC-5A / MLLCACSOA. Form does not specify the 1st-vs-2nd slot semantics — likely two parallel authorized signers per the converting entity's organic law (§1647 doesn't constrain).
- Open question: Reviewer collapsed drafter's two parallel booleans (conversion.has_organizing_document_exhibit, conversion.resulting_entity_not_filing_with_sos) into a single conversion.organizing_document_disposition enum to match the form's 'Select One' instruction (mutually exclusive). Cleaner XOR semantics for synth/rubric.
- Open question: Page-0 SIXTH foreign-resulting-entity address is two parallel widgets (Principal office address / Principal office address_2). Reviewer split into .line1 / .line2 sub-keys rather than .street / .city_state_zip because the form provides two unlabeled widgets without enforcing a street/city split — preserves the form's literal widget composition.
- Open question: Fee structure for §1647 conversions is not stated in the page-0 header (unlike MBCA-11I's $75 or MLLP-6's $175). Likely varies by resulting entity type (e.g., $175 LLC, $150 LP, $145 corp). Page-2 cover letter shows the fee field but the synth/rubric must cross-reference the resulting entity's organic-statute fee schedule. fee-* rubric check intentionally omitted at this pass-1 layer.
- Open question: FOURTH and FIFTH recitals on page 0 are static statutory affirmations (no fillable widget) — the conversion was approved as required by §1647 (FOURTH) and the converted organization's governing statute (FIFTH). No canonical key needed.
- Open question: Cross-reference: MBCA-21 (corporation conversion) has conversion.future_effective_date for OPTIONAL delayed effectiveness; MLLCCONV's THIRD recital (conversion.effective_date) is the actual MANDATORY effectiveness date. Both keys can coexist (different forms, different semantics).
