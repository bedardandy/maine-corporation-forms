# SKILL: Filling LP_MLPA-12

**Form:** Application for Certificate of Authority to Transact Business (Foreign Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Qualify a foreign limited partnership (LP, LLLP, or PLLLP) to transact business in Maine under 31 MRSA §1412. Records the home-jurisdiction name, an alternate Maine name when the home name lacks the required statutory suffix (FIRST), an optional fictitious-name election (SECOND), date and jurisdiction of organization (THIRD), principal-office address (FOURTH), required-office address in the home jurisdiction (FIFTH), Maine registered-agent appointment (SIXTH — commercial XOR noncommercial), the general-partner roster (EIGHTH — 3 inline rows + exhibit overflow), optional LLLP/PLLLP elections (NINTH/TENTH), and is signed on page 2 by an authorized general partner (with parallel entity-GP block).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | THIRD: Date of organization |
| `entity.home_jurisdiction` | text | high | Jurisdiction of organization |
| `entity.home_jurisdiction_name` | text | high | (Name of Limited Partnership in Jurisdiction of Organization) |
| `entity.is_lllp` | checkbox | high | NINTH: The foreign limited partnership is a limited liability limited partnership. |
| `entity.is_plllp` | checkbox | high | TENTH: This is a professional limited liability limited partnership... |
| `entity.maine_assumed_name_for_suffix` | text | high | FIRST: The proposed limited partnership name* to be used in this State |
| `entity.maine_fictitious_name` | text | high | SECOND: ...the fictitious name under which it proposes to apply for authority |
| `entity.principal_office.mailing_address` | text | high | FOURTH: (mailing address if different from above) |
| `entity.principal_office.physical_address` | text | high | FOURTH: The street and mailing address of the foreign limited partnership's principal office is: (physical location...) |
| `entity.professional_services_description.line1` | text | high | (provide the following professional services: ...) line 1 |
| `entity.professional_services_description.line2` | text | high | (provide the following professional services: ...) line 2 |

_Showing 12 of 45 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.maine_assumed_name_for_suffix is non-empty (FIRST is a required field) and contains one of: 'Limited Partnership', 'L.P.', or 'LP' (per 31 MRSA §1308.1.A.2 footnote on FIRST). (depends on `entity.maine_assumed_name_for_suffix`)
- If entity.maine_fictitious_name is non-empty, filing.fict4_accompanies must be true. (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- If entity.is_lllp is true, entity.maine_assumed_name_for_suffix must contain 'LLLP', 'L.L.L.P.', or 'Limited Liability Limited Partnership' (per the NINTH footnote, 31 MRSA §1308.1.A.3). (depends on `entity.is_lllp`, `entity.maine_assumed_name_for_suffix`)
- If entity.is_plllp is true, entity.maine_assumed_name_for_suffix must contain a professional suffix (e.g., 'chartered', 'professional limited liability limited partnership', 'P.L.L.L.P.', 'PLLLP') AND entity.professional_services_description.line1 must be non-empty. (depends on `entity.is_plllp`, `entity.maine_assumed_name_for_suffix`, `entity.professional_services_description.line1`)
- entity.home_jurisdiction is non-empty and is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is non-empty and on or before today. (depends on `entity.formation_date_in_home_jurisdiction`)
- entity.principal_office.physical_address is non-empty. (depends on `entity.principal_office.physical_address`)
- Exactly one of registered_agent.type values is selected (commercial XOR noncommercial). (depends on `registered_agent.type`)
- If registered_agent.type='commercial', registered_agent.cra_public_number must be non-empty. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address is non-empty and not a P.O. Box. (depends on `registered_agent.physical_address`)
- general_partner_1.name and general_partner_1.address are both non-empty (EIGHTH requires at least one inline GP). (depends on `general_partner_1.name`, `general_partner_1.address`)
- If general_partner.additional_attached is true, general_partner.additional_exhibit_letter must be non-empty. If false, all populated general_partner_N rows must have both name and address. (depends on `general_partner.additional_attached`, `general_partner.additional_exhibit_letter`, `general_partner_1.name`, `general_partner_1.address`, `general_partner_2.name`, `general_partner_2.address`, `general_partner_3.name`, `general_partner_3.address`)
- Either filing.signer.printed_name (individual GP signer) is non-empty, OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) are both non-empty (entity GP signer). (depends on `filing.signer.printed_name`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- ELEVENTH paragraph requires that an attached certificate of existence (or document of similar import) be dated within 90 days before delivery; cannot be auto-validated against widget data — track manually in filing.notes. (depends on )
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_assumed_name_for_suffix": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "home_jurisdiction": "Sample Value",
    "principal_office": {
      "physical_address": "Sample Value",
      "mailing_address": "Sample Value"
    }
  },
  "filing": {
    "fict4_accompanies": true
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999"
  }
}
```
