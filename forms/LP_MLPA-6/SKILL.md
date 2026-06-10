# SKILL: Filling LP_MLPA-6

**Form:** Certificate of Limited Partnership  
**Entity type:** Limited Partnership  
**When to use:** Form a Maine domestic limited partnership under 31 MRSA §1321, including LP name (or LLLP/PLLLP variant), designated-office address, registered agent, list of general partners, and optional series/professional designations.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.additional_provisions_exhibit_letter` | text | high | EIGHTH: ...are set forth in the attached Exhibit ___ |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.designated_office.mailing_address` | text | high | (mailing address if different from above) |
| `entity.designated_office.physical_address` | text | high | SECOND: (physical location - street (not P.O. Box), city, state and zip code) of designated office |
| `entity.is_lllp` | checkbox | high | SIXTH: [ ] The limited partnership is a limited liability limited partnership |
| `entity.is_professional_lllp` | checkbox | high | SEVENTH: [ ] This is a professional limited liability limited partnership formed pursuant to 31 MRSA §1354.4 |
| `entity.name` | text | high | FIRST: The name of the limited partnership is |
| `entity.professional_services_description` | text | high | (type of professional services) — line 1 (fills multiple widgets) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |

_Showing 12 of 44 canonical keys — the full set is in mapping.json._

## Conditional logic

- If entity.is_lllp is false: name contains 'Limited Partnership', 'L.P.' or 'LP'. If entity.is_lllp is true (and is_professional_lllp false): name contains 'L.L.L.P.', 'LLLP', or 'Limited Liability Limited Partnership' (no 'L.P.'/'LP'). If entity.is_professional_lllp is true: name contains 'PLLLP', 'P.L.L.L.P.', or 'S.L.L.L.P.'. (depends on `entity.name`, `entity.is_lllp`, `entity.is_professional_lllp`)
- entity.designated_office.physical_address is not a P.O. Box. (depends on `entity.designated_office.physical_address`)
- Exactly one of THIRD commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type = 'commercial', registered_agent.cra_public_number must be set. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address is not a P.O. Box. (depends on `registered_agent.physical_address`)
- At least one general_partner_N row is fully populated (name + address); LP requires ≥1 GP. (depends on `general_partner_1.name`, `general_partner_1.address`)
- If general_partner.additional_attached is true, general_partner.additional_exhibit_letter must be set. (depends on `general_partner.additional_attached`, `general_partner.additional_exhibit_letter`)
- Every populated general_partner_N has a corresponding signature/printed_name (individual block) OR appears as a general_partner_entity_N (entity block); certificate must be signed by all GPs per 31 MRSA §1321. (depends on `general_partner_1.name`, `general_partner_1.printed_name`, `general_partner_entity_1.name`)
- If entity.is_professional_lllp is true, entity.professional_services_description must be non-empty. (depends on `entity.is_professional_lllp`, `entity.professional_services_description`)
- If entity.is_professional_lllp is true, entity.is_lllp must also be true (PLLLP is a special case of LLLP). (depends on `entity.is_lllp`, `entity.is_professional_lllp`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "designated_office": {
      "physical_address": "Sample Value",
      "mailing_address": "Sample Value"
    }
  },
  "registered_agent": {
    "type": "Sample Value",
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value",
    "mailing_address": "Sample Value"
  }
}
```
