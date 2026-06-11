# SKILL: Filling LP_MLPA-12-1

**Form:** Application for Certificate of Authority to Transact Business (Foreign LP) — accompanying Application for Transfer of Authority  
**Entity type:** Limited Partnership  
**When to use:** Qualify a foreign limited partnership (LP, LLLP, or PLLLP) to transact business in Maine under 31 MRSA §1412 in connection with an Application for Transfer of Authority. The form (2 pages, 28 widgets) captures the proposed Maine name and required statutory suffix (FIRST), an optional fictitious-name election when the home name is unavailable in Maine (SECOND), LLLP / PLLLP status elections (THIRD/FOURTH), home-jurisdiction date and state of organization plus principal-office address (FIFTH), required-office address (SIXTH), Maine registered-agent appointment (SEVENTH/EIGHTH — commercial XOR noncommercial), and the general-partner roster (NINTH — 3 inline rows + exhibit overflow). TENTH paragraph requires that an attached certificate of existence is dated within 90 days before delivery. There is no cover letter or signature block on this form — those live on the accompanying Application for Transfer of Authority that this form bundles with.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.formation_date_in_home_jurisdiction` | text | high | FIFTH: Date of organization |
| `entity.home_jurisdiction` | text | high | FIFTH: Jurisdiction of organization |
| `entity.is_lllp` | checkbox | high | THIRD: …The foreign limited partnership is a limited liability limited partnership. |
| `entity.is_plllp` | checkbox | high | FOURTH: …This is a professional limited liability limited partnership** qualified pursuant to 31 MRSA §1354.4. |
| `entity.maine_assumed_name_for_suffix` | text | high | FIRST: The proposed limited partnership name* to be used in this State |
| `entity.maine_fictitious_name` | text | high | SECOND: …the fictitious name under which it proposes to apply for authority to do business in the State of Maine is |
| `entity.principal_office.mailing_address` | text | high | FIFTH: (mailing address if different from above) |
| `entity.principal_office.physical_address` | text | high | FIFTH: The street and mailing address of the foreign limited partnership's principal office is: (physical location, street – not P.O. Box, city, state and zip code) |
| `entity.professional_services_description.line1` | text | high | (provide the following professional services: ...) line 1 |
| `entity.professional_services_description.line2` | text | high | (provide the following professional services: ...) line 2 |
| `entity.required_office.mailing_address` | text | high | SIXTH: (mailing address if different from above) |
| `entity.required_office.physical_address` | text | high | SIXTH: The street and mailing address of the foreign limited partnership's required office is: (physical location, street – not P.O. Box, city, state and zip code) |

_Showing 12 of 26 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.maine_assumed_name_for_suffix is non-empty (FIRST). (depends on `entity.maine_assumed_name_for_suffix`)
- entity.maine_assumed_name_for_suffix contains one of: 'Limited Partnership', 'L.P.', or 'LP' (per 31 MRSA §1308.1.A.2 footnote on FIRST). (depends on `entity.maine_assumed_name_for_suffix`)
- If entity.maine_fictitious_name is non-empty, filing.fict4_accompanies must be true. (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- If entity.is_lllp is true, entity.maine_assumed_name_for_suffix must contain 'LLLP' or 'L.L.L.P.' (per the THIRD footnote, 31 MRSA §1308.1.A.3). (depends on `entity.is_lllp`, `entity.maine_assumed_name_for_suffix`)
- If entity.is_plllp is true, entity.maine_assumed_name_for_suffix must contain a 'professional' suffix (e.g., 'chartered', 'professional limited liability limited partnership', 'P.L.L.L.P.', 'PLLLP') per the FOURTH footnote, and entity.professional_services_description.line1 must be non-empty. (depends on `entity.is_plllp`, `entity.maine_assumed_name_for_suffix`, `entity.professional_services_description.line1`)
- entity.home_jurisdiction is non-empty and is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is non-empty and on or before today. (depends on `entity.formation_date_in_home_jurisdiction`)
- entity.principal_office.physical_address is non-empty and not a P.O. Box. (depends on `entity.principal_office.physical_address`)
- Exactly one of registered_agent.type values is selected (commercial XOR noncommercial). (depends on `registered_agent.type`)
- If registered_agent.type = 'commercial', registered_agent.cra_public_number must be non-empty. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address is non-empty and not a P.O. Box. (depends on `registered_agent.physical_address`)
- general_partner_1.name and general_partner_1.address are both non-empty (NINTH requires at least one inline GP). (depends on `general_partner_1.name`, `general_partner_1.address`)
- If general_partner.additional_attached is true, general_partner.additional_exhibit_letter must be non-empty. If false, all populated general_partner_N rows must have both name and address. (depends on `general_partner.additional_attached`, `general_partner.additional_exhibit_letter`, `general_partner_1.name`, `general_partner_1.address`, `general_partner_2.name`, `general_partner_2.address`, `general_partner_3.name`, `general_partner_3.address`)

## Example case data

```json
{
  "entity": {
    "maine_assumed_name_for_suffix": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "is_lllp": true,
    "is_plllp": true,
    "professional_services_description": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "formation_date_in_home_jurisdiction": "2026-01-15"
  },
  "filing": {
    "fict4_accompanies": "Sample Value"
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999"
  }
}
```
