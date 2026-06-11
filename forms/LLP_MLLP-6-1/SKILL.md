# SKILL: Filling LLP_MLLP-6-1

**Form:** Certificate of Limited Liability Partnership — accompanying entity-action filing  
**Entity type:** Limited Liability Partnership  
**When to use:** File a Certificate of Limited Liability Partnership pursuant to 31 MRSA §822 in connection with one of five underlying entity-action filings that produces an LLP as the resulting entity: Articles of Entity Conversion (13-C MRSA §955.1), Articles/Certificate of Merger or Share Exchange (13-C MRSA §1106 / 31 MRSA §744 / 31 MRSA §1436), Certificate of Inter-Entity Consolidation (31 MRSA §744), Articles/Certificate of Conversion (31 MRSA §746 / 31 MRSA §1432), or Articles of Conversion of Partnership (31 MRSA §1093). The form (2 pages, 19 widgets) captures the LLP name (FIRST), the Maine registered agent (SECOND — commercial XOR noncommercial; THIRD is a static §108.3 consent recital with no widget), the optional professional-LLP election with services description (FOURTH), the contact partner block (FIFTH), and an exhibit letter for additional provisions (SIXTH). There is no cover letter or signature block on this form — those live on the accompanying underlying filing.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `contact_partner.address` | text | high | FIFTH: ... Address |
| `contact_partner.name` | text | high | FIFTH: The name and business, residence or mailing address of the contact partner is: Name |
| `entity.additional_provisions_exhibit_letter` | text | high | SIXTH: Other provisions of this certificate, if any, that the partners determine to include are set forth in Exhibit ___ attached hereto and made a part hereof. |
| `entity.is_professional_llp` | checkbox | high | FOURTH: This is a professional limited liability partnership* formed pursuant to 13 MRSA, chapter 22-A to provide the following professional services |
| `entity.name` | text | high | FIRST: The name of the registered limited liability partnership is — must contain 'Limited Liability Partnership', 'L.L.P.' or 'LLP' (per 31 MRSA §803-A) |
| `entity.professional_services_description.line1` | text | high | FOURTH: (type of professional services) line 1 |
| `entity.professional_services_description.line2` | text | high | FOURTH: (type of professional services) line 2 |
| `filing.underlying_filing_type` | enum_select | high | Articles of Entity Conversion (13-C MRSA §955.1) [option 1] |
| `registered_agent.cra_public_number` | text | high | SECOND: CRA Public Number (alongside Commercial Registered Agent radio) |
| `registered_agent.mailing_address` | text | high | SECOND: (mailing address if different from above) |
| `registered_agent.name` | text | high | SECOND: (name of commercial registered agent) (fills multiple widgets) |
| `registered_agent.physical_address` | text | high | SECOND: (physical location, not P.O. Box – street, city, state and zip code) |

_Showing 12 of 13 canonical keys — the full set is in mapping.json._

## Conditional logic

- Exactly one filing.underlying_filing_type enum value is selected (one of five page-0 checkboxes). (depends on `filing.underlying_filing_type`)
- entity.name is non-empty and contains 'Limited Liability Partnership', 'L.L.P.', or 'LLP' (per 31 MRSA §803-A). (depends on `entity.name`)
- Exactly one of registered_agent.type values is selected (commercial XOR noncommercial). (depends on `registered_agent.type`)
- If registered_agent.type = 'commercial', registered_agent.cra_public_number must be non-empty. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.name is non-empty. (depends on `registered_agent.name`)
- registered_agent.physical_address is non-empty and not a P.O. Box. (depends on `registered_agent.physical_address`)
- If entity.is_professional_llp is true, at least entity.professional_services_description.line1 must be non-empty. (depends on `entity.is_professional_llp`, `entity.professional_services_description.line1`)
- contact_partner.name and contact_partner.address are both non-empty (FIFTH). (depends on `contact_partner.name`, `contact_partner.address`)
- If entity.additional_provisions_exhibit_letter is populated, it must be a single uppercase letter A-Z. (depends on `entity.additional_provisions_exhibit_letter`)

## Example case data

```json
{
  "filing": {
    "underlying_filing_type": "articles_of_entity_conversion"
  },
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "is_professional_llp": true
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value",
    "mailing_address": "Sample Value"
  }
}
```
