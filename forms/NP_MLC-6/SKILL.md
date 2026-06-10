# SKILL: Filling NP_MLC-6

**Form:** Certificate of Organization (Domestic Nonprofit Corporation Independent Local Church)  
**Entity type:** Nonprofit Corporation  
**When to use:** Form a Maine domestic nonprofit corporation organized as an independent local church under 13 MRSA §3021. Records the church's name, the Maine city/town where it is located, the number of trustees and an inline trustees-named recital (THIRD), and the named-and-addressed officers (Clerk, Treasurer) and Trustees who execute the certificate. Filing fee is $5.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `clerk.address.city_state_zip` | text | high | (city, state and zip code) — lower-right of Clerk block |
| `clerk.address.street` | text | high | Street ___ (upper-right of Clerk block) |
| `clerk.printed_name` | text | high | (Clerk) / (type or print name) — lower-left of Clerk block |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.location_city` | text | high | SECOND: The corporation is an independent local church located in ___, Maine. |
| `entity.name` | text | high | FIRST: The name of the church is |
| `entity.trustee_count` | text | high | THIRD: The number of trustees is ___ |
| `entity.trustee_names_inline` | text | high | and their names are ___ (continuation line 1 of THIRD recital) (fills multiple widgets) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |

_Showing 12 of 40 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.location_city is non-empty. (depends on `entity.location_city`)
- entity.trustee_count is non-empty and a positive integer. (depends on `entity.trustee_count`)
- entity.trustee_names_inline is non-empty (THIRD recital lists the trustees in prose). (depends on `entity.trustee_names_inline`)
- clerk.printed_name is non-empty. (depends on `clerk.printed_name`)
- clerk.address.street and clerk.address.city_state_zip are non-empty. (depends on `clerk.address.street`, `clerk.address.city_state_zip`)
- treasurer.printed_name is non-empty. (depends on `treasurer.printed_name`)
- treasurer.address.street and treasurer.address.city_state_zip are non-empty. (depends on `treasurer.address.street`, `treasurer.address.city_state_zip`)
- trustee_1.printed_name is non-empty (at minimum, the form requires one trustee block populated; entity.trustee_count should match the count of populated trustee_N blocks plus any spilled to attached pages). (depends on `trustee_1.printed_name`, `entity.trustee_count`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "location_city": "Sample Value",
    "trustee_count": 100,
    "trustee_names_inline": "Wabanaki Widgets, Inc."
  },
  "filing": {
    "date_signed": "2026-01-15"
  },
  "clerk": {
    "printed_name": "Sample Value",
    "address": {
      "street": "Sample Value",
      "city_state_zip": "Sample Value"
    }
  },
  "treasurer": {}
}
```
