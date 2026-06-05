# SKILL: Filling LLP_MLLP-9

**Form:** Certificate of Amendment (Domestic Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Amend the certificate of a Maine domestic Limited Liability Partnership under 31 MRSA §823. Captures (FIRST) a name change with mandatory LLP suffix, (SECOND) a change to the contact partner's name and/or address, and (THIRD) any other amendments via attached exhibit.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.new_entity_name` | text | high | FIRST: The name of the limited liability partnership has been changed to (if no change, so indicate) |
| `amendment.other_exhibit_letter` | text | high | THIRD: Other amendments to the certificate ... are set forth in Exhibit ___ attached hereto |
| `contact_partner.address` | text | high | SECOND: ... contact partner has been changed to ... Address |
| `contact_partner.name` | text | high | SECOND: ... contact partner has been changed to ... Name |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Limited Liability Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |

## Conditional logic

- entity.name (the LLP's current name) is non-empty. (depends on `entity.name`)
- If amendment.new_entity_name is populated and not 'no change', it must contain one of 'Limited Liability Partnership', 'L.L.P.', or 'LLP' (per 31 MRSA §803-A). (depends on `amendment.new_entity_name`)
- If amendment.other_exhibit_letter is populated, it must be a single uppercase letter A-Z. (depends on `amendment.other_exhibit_letter`)
- Exactly one signer block is populated: either filing.signer.printed_name_and_capacity (individual partner) OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) (entity partner). (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is on or before today. (depends on `filing.date_signed`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name matches entity.name (or amendment.new_entity_name if changed). (depends on `filing.entities[0].name`, `entity.name`, `amendment.new_entity_name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "amendment": {
    "new_entity_name": "Sample Value",
    "other_exhibit_letter": "Sample Value"
  },
  "contact_partner": {
    "name": "Sample Value",
    "address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "signer_entity": {
      "name": "Sample Value"
    }
  }
}
```
