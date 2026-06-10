# SKILL: Filling CORP_MERGFOR

**Form:** Merger (Foreign Entities)  
**Entity type:** Business Corporation  
**When to use:** Record with the Maine SOS a merger involving foreign entities where at least one party is qualified or registered in Maine. The form captures the surviving foreign entity's home name, jurisdiction, Maine-authorization date, and any post-merger name change; and the nonsurviving foreign entity's home name, jurisdiction, and Maine-authorization date. A certified copy of the merger (or certificate of merger) from the home jurisdiction must be attached. Per the page-1 fee table the filing fee depends on the entity type ($25 for foreign nonprofit; $100 for foreign business corporation; $150 for foreign LP/foreign LLP under 31 MRSA §1411 / §1438).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity(s) on the submitted filings [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- merger.surviving_entity.home_jurisdiction_name is non-empty. (depends on `merger.surviving_entity.home_jurisdiction_name`)
- merger.surviving_entity.home_jurisdiction is non-empty and is not 'Maine' (the form is for foreign entities). (depends on `merger.surviving_entity.home_jurisdiction`)
- merger.nonsurviving_entity.home_jurisdiction_name is non-empty. (depends on `merger.nonsurviving_entity.home_jurisdiction_name`)
- merger.nonsurviving_entity.home_jurisdiction is non-empty. (depends on `merger.nonsurviving_entity.home_jurisdiction`)
- At least one of merger.surviving_entity.maine_authorization_date or merger.nonsurviving_entity.maine_authorization_date is non-empty (the merger is filed in Maine because at least one party touches Maine). (depends on `merger.surviving_entity.maine_authorization_date`, `merger.nonsurviving_entity.maine_authorization_date`)
- merger.certified_copy_attached is true (the form requires a certified copy of the merger from the home jurisdiction). (depends on `merger.certified_copy_attached`)
- filing.entities[0].name matches merger.surviving_entity.home_jurisdiction_name (or merger.surviving_entity.new_name when populated). (depends on `filing.entities[0].name`, `merger.surviving_entity.home_jurisdiction_name`, `merger.surviving_entity.new_name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "merger": {
    "surviving_entity": {
      "home_jurisdiction_name": "Sample Value",
      "home_jurisdiction": "Sample Value",
      "maine_authorization_date": "2026-01-15",
      "new_name": "Sample Value"
    },
    "nonsurviving_entity": {
      "home_jurisdiction_name": "Sample Value",
      "home_jurisdiction": "Sample Value",
      "maine_authorization_date": "2026-01-15"
    }
  },
  "filing": {
    "entities": [
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
