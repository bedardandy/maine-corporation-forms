# LLP_MLLP-6A — Restated Certificate of Limited Liability Partnership

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 35  
**Mapped fields:** 31  
**Filer role:** at least one partner OR any duly authorized person (per page-1 footnote: '*Certificate MUST be signed by: (1) at least one partner OR (2) any duly authorized person')

## Purpose

File a Restated Certificate of Limited Liability Partnership for a domestic Maine LLP under 31 MRSA §823.6. Captures (FIRST) any change to the LLP name, (SECOND) the date and original name of the initial certificate, (THIRD) the registered agent (commercial or noncommercial), (FIFTH) the contact partner block, (SIXTH) any other restated provisions via attached exhibit, and the partner signature block (up to 2 individual partners + 2 entity partners inline).

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

- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: FIRST instructs the filer to write 'no change' literally if the name is not being amended (same convention as MLLP-9). Synth must emit either 'no change' or a valid suffix-bearing name.
- Open question: Form has TWO inline individual-partner signature slots (Text14, Text15) and TWO inline entity-partner signature blocks (Text16/17, Text18/19). Drafter introduces partner_N.* and partner_entity_N.* (N=1..2) as a multi-slot pattern parallel to MLPA-6's general_partner_N.* — distinct from MLLP-9's single-signer filing.signer.*. Confirm whether overflow beyond slot 2 is anticipated (form does not have an opt-in 'additional partners attached' checkbox like MLLP-12's manager.additional_attached).
- Open question: Page-0 SECOND has no 'no change' sentinel for entity.original_articles_filing_date or entity.original_name — these are mandatory disclosures on every restated certificate (the form's purpose is to restate, so the original filing details are always present).
- Open question: Page-1 footnote allows '(2) any duly authorized person' to sign (alternative to a partner). Schema currently has no key for 'duly authorized non-partner signer'. If such a signer fills Text14, partner_1.printed_name_and_capacity will hold a non-partner signer's name+capacity — the rubric should accept this since the form does not distinguish the two paths via separate widgets.
- Open question: Form has no widget for the 'FOURTH' recital ('Pursuant to 5 MRSA §108.3, the registered agent so listed above has consented to serve...') — it is a static statutory recital with no fillable field, only a checkbox-free declaration.
