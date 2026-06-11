# SKILL: Filling LP_MLPA-6-1

**Form:** Certificate of Limited Partnership — accompanying a transaction (Conversion / Merger / Consolidation)  
**Entity type:** Limited Partnership  
**When to use:** Form a Maine domestic limited partnership under 31 MRSA §1321 in connection with one of five accompanying transactions (Articles of Entity Conversion, Articles/Certificate of Merger or Share Exchange, Certificate of Inter-Entity Consolidation, Articles/Certificate of Conversion, Articles of Conversion of Partnership). The form (2 pages, 28 widgets) captures: a five-option transaction-type election (top of page 1, 'X one box only'), the LP name with required suffix (FIRST), designated-office physical/mailing addresses (SECOND), Maine registered-agent appointment (THIRD — commercial XOR noncommercial; FOURTH paragraph confirms agent consent), the general-partner roster (FIFTH — 3 inline rows + exhibit overflow), optional LLLP elect-in (SIXTH), optional PLLLP elect-in plus 2-line professional-services description (SEVENTH), and an optional additional-provisions exhibit letter (EIGHTH). There is no cover letter, no signature block, and no date_signed widget on this form — those live on the accompanying transaction filing (e.g., MBCA-21, MLPA-9, MLPA-17) that this form bundles with. Same '-1' bundled-sheet pattern as LP_MLPA-12-1 and LLP_MLLP-12-1.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.additional_provisions_exhibit_letter` | text | high | EIGHTH: ...are set forth in the attached Exhibit ___ and made a part hereof |
| `entity.designated_office.mailing_address` | text | high | (mailing address if different from above) |
| `entity.designated_office.physical_address` | text | high | SECOND: The street and mailing address of the limited partnership's designated office shall be (physical location, street – not P.O. Box, city, state and zip code) |
| `entity.is_lllp` | checkbox | high | SIXTH: The limited partnership is a limited liability limited partnership |
| `entity.is_professional_lllp` | checkbox | high | SEVENTH: This is a professional limited liability limited partnership formed pursuant to 31 MRSA §1354.4 |
| `entity.name` | text | high | FIRST: The name of the limited partnership is |
| `entity.professional_services_description` | text | high | (provide the following professional services) — line 1 (fills multiple widgets) |
| `filing.accompanying_transaction_type` | text | high | Articles of Entity Conversion (13-C MRSA §955.1) (fills multiple widgets) |
| `general_partner.additional_attached` | text | high | Names and addresses of additional general partners are attached as Exhibit ___ and made a part hereof |
| `general_partner.additional_exhibit_letter` | text | high | Exhibit ___ [additional general partners] |
| `general_partner_1.address` | text | high | FIFTH: Address (general partner row 1) |
| `general_partner_1.name` | text | high | FIFTH: Name (general partner row 1) |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- Exactly one of the five top-of-form transaction-type checkboxes is selected ('X one box only'). (depends on `filing.accompanying_transaction_type`)
- If entity.is_lllp is false: name contains 'Limited Partnership', 'L.P.', or 'LP'. If entity.is_lllp is true (and is_professional_lllp false): name contains 'L.L.L.P.', 'LLLP', or 'Limited Liability Limited Partnership' (no 'L.P.'/'LP'). If entity.is_professional_lllp is true: name contains 'PLLLP', 'P.L.L.L.P.', or 'S.L.L.L.P.'. (depends on `entity.name`, `entity.is_lllp`, `entity.is_professional_lllp`)
- entity.designated_office.physical_address is non-empty and not a P.O. Box. (depends on `entity.designated_office.physical_address`)
- Exactly one of THIRD commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type='commercial', registered_agent.cra_public_number must be non-empty. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address is non-empty and not a P.O. Box. (depends on `registered_agent.physical_address`)
- general_partner_1.name and general_partner_1.address are both non-empty (FIFTH requires ≥1 inline GP; LP must have ≥1 GP per 31 MRSA §1321). (depends on `general_partner_1.name`, `general_partner_1.address`)
- If general_partner.additional_attached is true, general_partner.additional_exhibit_letter must be non-empty. If false, all populated general_partner_N rows must have both name and address (no half-rows). (depends on `general_partner.additional_attached`, `general_partner.additional_exhibit_letter`, `general_partner_1.name`, `general_partner_1.address`, `general_partner_2.name`, `general_partner_2.address`, `general_partner_3.name`, `general_partner_3.address`)
- If entity.is_professional_lllp is true, entity.professional_services_description must be non-empty (after concatenating Text15+Text16). (depends on `entity.is_professional_lllp`, `entity.professional_services_description`)
- If entity.is_professional_lllp is true, entity.is_lllp must also be true (PLLLP is a special case of LLLP). (depends on `entity.is_lllp`, `entity.is_professional_lllp`)

## Example case data

```json
{
  "filing": {
    "accompanying_transaction_type": "entity_conversion_13c"
  },
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "designated_office": {
      "physical_address": "Sample Value",
      "mailing_address": "Sample Value"
    }
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value"
  }
}
```
