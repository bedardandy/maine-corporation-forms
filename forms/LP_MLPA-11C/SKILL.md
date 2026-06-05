# SKILL: Filling LP_MLPA-11C

**Form:** Statement of Termination (Domestic Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Terminate a Maine domestic limited partnership pursuant to 31 MRSA §1323. Records the original certificate filing date, optional additional information via exhibit, and the signatures of all general partners (individuals or authorized representatives of entity GPs) winding up the partnership.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Limited Partnership) |
| `entity.original_certificate_filing_date` | text | high | FIRST: The date the original certificate of limited partnership was filed |
| `filing.additional_info_exhibit_letter` | text | high | SECOND: …set forth in Exhibit ___ attached hereto |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | Dated ___ |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.original_certificate_filing_date is non-empty. (depends on `entity.original_certificate_filing_date`)
- filing.date_signed is on or after entity.original_certificate_filing_date — cannot terminate before formation. (depends on `filing.date_signed`, `entity.original_certificate_filing_date`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- At least one GP slot is signed: any of general_partner_{1..3}.printed_name OR general_partner_entity_1.signer_printed_name_and_capacity is non-empty (§1323 strictly requires all GPs sign; rubric loosens to ≥1 since synth may model partial-fill states). (depends on `general_partner_1.printed_name`, `general_partner_2.printed_name`, `general_partner_3.printed_name`, `general_partner_entity_1.signer_printed_name_and_capacity`)
- If general_partner_entity_1.signer_printed_name_and_capacity is non-empty, general_partner_entity_1.name must also be non-empty. (depends on `general_partner_entity_1.name`, `general_partner_entity_1.signer_printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.expedited_service is exactly one of hold_for_pickup | 24h_next_business_day | immediate_same_day. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "original_certificate_filing_date": "2026-01-15"
  },
  "filing": {
    "additional_info_exhibit_letter": "Sample Value",
    "date_signed": "2026-01-15"
  },
  "general_partner_1": {
    "printed_name": "Sample Value"
  },
  "general_partner_2": {
    "printed_name": "Sample Value"
  },
  "general_partner_3": {
    "printed_name": "Sample Value"
  },
  "general_partner_entity_1": {
    "name": "Sample Value"
  }
}
```
