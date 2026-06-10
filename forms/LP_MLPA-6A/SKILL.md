# SKILL: Filling LP_MLPA-6A

**Form:** Restated Certificate of Limited Partnership  
**Entity type:** Limited Partnership  
**When to use:** Restate the Certificate of Limited Partnership for an existing Maine domestic limited partnership under 31 MRSA §1322.5. Records the LP's current name (as on file with SOS), any new name, the initial filing date, designated-office address, registered agent (commercial or noncommercial), updated general-partner roster (3 inline rows + exhibit overflow), optional LLLP/professional-LLLP elections, and dual signature blocks for individual GPs (page 1) and entity GPs (page 2).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.designated_office.physical_address` | text | high | THIRD: The street and mailing address of the limited partnership's designated office shall be: (physical location – street (not P.O. Box), city, state and zip code) |
| `entity.initial_filing_date` | text | high | SECOND: The date of filing of the initial certificate of limited partnership was |
| `entity.is_lllp` | checkbox | high | SEVENTH: Check only if applicable [ ] The limited partnership is a limited liability limited partnership. |
| `entity.name` | text | high | (Name of Limited Partnership as it appears on the record of the Secretary of State) |
| `entity.new_name` | text | high | FIRST: The name of the limited partnership has been changed to (if no change, so indicate): |
| `entity.professional_services_description` | text | high | EIGHTH: This is a professional limited liability limited partnership* formed pursuant to 31 MRSA §1354.4 to provide the following professional services: (type of professional services) — line 1 (fills multiple widgets) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |

_Showing 12 of 42 canonical keys — the full set is in mapping.json._

## Conditional logic

- Both entity.name (current name as on SOS record) and entity.new_name are non-empty. If filer intends no name change, entity.new_name should equal entity.name OR contain a 'no change' marker. (depends on `entity.name`, `entity.new_name`)
- entity.initial_filing_date is a valid date and not in the future relative to filing.date_signed. (depends on `entity.initial_filing_date`, `filing.date_signed`)
- entity.designated_office.physical_address must not begin with 'P.O.', 'PO Box', or 'Post Office Box'. (depends on `entity.designated_office.physical_address`)
- Exactly one of FOURTH registered_agent.type options is selected (commercial XOR noncommercial). (depends on `registered_agent.type`)
- If registered_agent.type='commercial', registered_agent.cra_public_number must be set; if 'noncommercial', it must be absent. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address must not begin with 'P.O.', 'PO Box', or 'Post Office Box'. (depends on `registered_agent.physical_address`)
- At least one general_partner_N (individual or entity) is fully populated; LP requires ≥1 GP per 31 MRSA §1322.5. (depends on `general_partner_1.name`, `general_partner_1.address`, `general_partner_entity_1.name`)
- If general_partner_N.name is non-empty, general_partner_N.address must also be non-empty (and vice versa). (depends on `general_partner_1.name`, `general_partner_1.address`, `general_partner_2.name`, `general_partner_2.address`, `general_partner_3.name`, `general_partner_3.address`)
- Each populated general_partner_N (individual) has a corresponding general_partner_N.printed_name on the page-1 signature block; certificate must be signed by all GPs. (depends on `general_partner_1.name`, `general_partner_1.printed_name`, `general_partner_2.name`, `general_partner_2.printed_name`, `general_partner_3.name`, `general_partner_3.printed_name`)
- Each populated general_partner_entity_N has a corresponding signer_printed_name_and_capacity on the page-2 entity-GP block. (depends on `general_partner_entity_1.name`, `general_partner_entity_1.signer_printed_name_and_capacity`, `general_partner_entity_2.name`, `general_partner_entity_2.signer_printed_name_and_capacity`, `general_partner_entity_3.name`, `general_partner_entity_3.signer_printed_name_and_capacity`)
- If entity.is_lllp is true, entity.new_name must contain 'L.L.L.P.', 'LLLP', or 'Limited Liability Limited Partnership' and must NOT contain 'L.P.' or 'LP' (per 31 MRSA §1308.1.A.3). (depends on `entity.is_lllp`, `entity.new_name`)
- If entity.professional_services_description is non-empty (EIGHTH professional-LLLP election checked), entity.is_lllp must be true (PLLLP is a special case of LLLP per §1354.4). (depends on `entity.professional_services_description`, `entity.is_lllp`)
- filing.date_signed is not in the future relative to the submission date. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "new_name": "Wabanaki Widgets, Inc.",
    "initial_filing_date": "2026-01-15",
    "designated_office": {
      "physical_address": "Sample Value"
    }
  },
  "registered_agent": {
    "type": "Sample Value",
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value"
  }
}
```
