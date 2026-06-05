# SKILL: Filling CORP_MBCA-15

**Form:** Application for the Use of an Indistinguishable Name  
**Entity type:** Business Corporation  
**When to use:** Allow a Maine business corporation that holds rights to a name to consent to another applicant's use of an indistinguishable name under 13-C MRSA §401.4. The consenting corporation simultaneously commits to changing its own name to a distinguishable form. Per the form's footnote, this application MUST be accompanied by the applicable name-change form (Articles of Amendment, MBCA-9) carrying the new distinguishable name.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation Allowing Indistinguishable Name) |
| `entity.new_distinguishable_name` | text | high | THIRD: The entity in possession of the name must change its name to:* |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

## Conditional logic

- entity.name is non-empty (the consenting corporation's current Maine name). (depends on `entity.name`)
- indistinguishable_name.proposed_name is non-empty. (depends on `indistinguishable_name.proposed_name`)
- indistinguishable_name.requestor_name is non-empty. (depends on `indistinguishable_name.requestor_name`)
- entity.new_distinguishable_name is non-empty (consenting corp commits to a new name). (depends on `entity.new_distinguishable_name`)
- entity.new_distinguishable_name differs from entity.name and from indistinguishable_name.proposed_name (otherwise the consent is vacuous). (depends on `entity.name`, `entity.new_distinguishable_name`, `indistinguishable_name.proposed_name`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.expedited_service is exactly one of hold_for_pickup | 24h_next_business_day | immediate_same_day. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "new_distinguishable_name": "Wabanaki Widgets, Inc."
  },
  "indistinguishable_name": {
    "proposed_name": "Sample Value",
    "requestor_name": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    }
  }
}
```
