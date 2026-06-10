# SKILL: Filling LLP_MLLP-6A

**Form:** Restated Certificate of Limited Liability Partnership  
**Entity type:** Limited Liability Partnership  
**When to use:** File a Restated Certificate of Limited Liability Partnership for a domestic Maine LLP under 31 MRSA §823.6. Captures (FIRST) any change to the LLP name, (SECOND) the date and original name of the initial certificate, (THIRD) the registered agent (commercial or noncommercial), (FIFTH) the contact partner block, (SIXTH) any other restated provisions via attached exhibit, and the partner signature block (up to 2 individual partners + 2 entity partners inline).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.new_entity_name` | text | high | FIRST: The name of the limited liability partnership has been changed to (if no change, so indicate) |
| `contact_partner.address` | text | high | FIFTH: ... Address |
| `contact_partner.name` | text | high | FIFTH: The name and business, residence or mailing address of the contact partner is: Name |
| `entity.additional_provisions_exhibit_letter` | text | high | SIXTH: Other provisions of this restated certificate, if any, that the partners determine to include are set forth in Exhibit ___ attached hereto and made a part hereof. |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Limited Liability Partnership as it appears on the record of the Secretary of State) |
| `entity.original_articles_filing_date` | text | high | SECOND: The date of filing of the initial certificate of limited liability partnership was |
| `entity.original_name` | text | high | SECOND (continued): The name under which it was originally filed was: |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |

_Showing 12 of 33 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the LLP's current SOS-recorded name) is non-empty. (depends on `entity.name`)
- If amendment.new_entity_name is populated and not 'no change', it must contain one of 'Limited Liability Partnership', 'L.L.P.', or 'LLP' (per 31 MRSA §803-A). (depends on `amendment.new_entity_name`)
- Both entity.original_articles_filing_date and entity.original_name are populated (SECOND recital is two interdependent fields). (depends on `entity.original_articles_filing_date`, `entity.original_name`)
- entity.original_articles_filing_date is on or before filing.date_signed. (depends on `entity.original_articles_filing_date`, `filing.date_signed`)
- Exactly one of THIRD commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- registered_agent.name and registered_agent.physical_address are non-empty. (depends on `registered_agent.name`, `registered_agent.physical_address`)
- If registered_agent.type='commercial', registered_agent.cra_public_number must be set. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- contact_partner.name and contact_partner.address are non-empty (FIFTH recital). (depends on `contact_partner.name`, `contact_partner.address`)
- If entity.additional_provisions_exhibit_letter is populated, it must be a single uppercase letter A-Z. (depends on `entity.additional_provisions_exhibit_letter`)
- At least one of {partner_1.printed_name_and_capacity, partner_2.printed_name_and_capacity, partner_entity_1.signer_printed_name_and_capacity, partner_entity_2.signer_printed_name_and_capacity} is non-empty (per page-1 footnote requirement). (depends on `partner_1.printed_name_and_capacity`, `partner_2.printed_name_and_capacity`, `partner_entity_1.signer_printed_name_and_capacity`, `partner_entity_2.signer_printed_name_and_capacity`)
- If partner_entity_N.name is populated, partner_entity_N.signer_printed_name_and_capacity must also be populated (and vice versa) — the entity-partner block has two interdependent widgets per slot. (depends on `partner_entity_1.name`, `partner_entity_1.signer_printed_name_and_capacity`, `partner_entity_2.name`, `partner_entity_2.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name (or amendment.new_entity_name if a name change is being effected). (depends on `filing.entities[0].name`, `entity.name`, `amendment.new_entity_name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "original_articles_filing_date": "2026-01-15",
    "original_name": "Wabanaki Widgets, Inc."
  },
  "amendment": {
    "new_entity_name": "Sample Value"
  },
  "registered_agent": {
    "type": "Sample Value",
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value"
  }
}
```
