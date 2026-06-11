# LLP_MLLP-6 — Certificate of Limited Liability Partnership

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 38  
**Mapped fields:** 34  
**Filer role:** one or more partners who are authorized OR any duly authorized person (per the page-1 footnote: '**Certificate MUST be signed by: (1) one or more partners who are authorized OR (2) any duly authorized person'). Signer block uses the per-officer multi-slot pattern partner_N.* / partner_entity_N.* (mirrors MLLP-6A's restated-certificate signer block).

## Purpose

Form a domestic Maine Limited Liability Partnership under 31 MRSA §822 (also referenced on the form as the LLP qualification statement). Captures: optional professional-LLP election under 13 MRSA Chapter 22-A; the LLP's name (with statutory suffix per §803-A); registered agent (commercial or noncommercial) with physical and optional mailing address; the contact partner's name and address; an optional additional-provisions exhibit; and up to 3 individual-partner signature slots plus 3 entity-partner signature slots.

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
- Open question: FOURTH section provides BOTH an inline combined widget (Text8) and split Name/Address columns (Text9/Text10). Likely a redundant template layout — synth should populate the split widgets (matching MLLP-6A's contact_partner.name / contact_partner.address convention) and either leave Text8 empty or derive it. Confirm whether the filler engine mirrors split→combined automatically or treats Text8 as an independent field.
- Open question: Page-1 footnote allows '(2) any duly authorized person' to sign — alternative to a partner. When such a non-partner signer fills Text12-14, partner_1.printed_name will hold a non-partner signer's name (no separate canonical key for 'duly authorized non-partner signer' on this multi-slot pattern; the rubric accepts this since the form does not distinguish the two paths via separate widgets).
- Open question: Form provides 3 inline individual-partner slots and 3 inline entity-partner slots — same shape as MLPA-6 (LP formation) which uses general_partner_N.* / general_partner_entity_N.*. MLLP-6 uses partner_N.* / partner_entity_N.* (LLP terminology) per the schema-gap convention from MLLP-6A.
- Open question: Drafter's filer_role description called this an 'LLP qualification statement to convert a domestic limited partnership'. Reviewer revised: §822 governs LLP formation/qualification (a partnership becomes an LLP via this filing, but the filer is the partnership itself; this is not a LP→LLP merger or conversion in the §1647 sense). The form is a Certificate of LLP — formation-style filing for a domestic Maine LLP.
- Open question: Drafter mapped 'professional services description' to entity.professional_services_description (correct, reuses MLPA-6 key) but the schema_gap entry was missing; reviewer added.
- Open question: No AcroForm signature widgets on the wet-ink (signature) lines under Partner(s)** or 'By' lines under entity-partner blocks — signatures are wet-ink/image overlays. Consistent with MLLP-6A and the broader filer-engine convention.
