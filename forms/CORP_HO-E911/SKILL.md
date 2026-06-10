# SKILL: Filling CORP_HO-E911

**Form:** Notification of Change in Home Office Address by Municipality or U.S. Postal Service  
**Entity type:** Business Corporation  
**When to use:** Notify the Maine Secretary of State of a change in a foreign entity's home-office address caused by a municipality or U.S. Postal Service action (e.g., E-911 street renumbering or USPS-imposed mailing-address change). Filed by a foreign business corporation, LLC, LP, or LLP that has been authorized to transact business in Maine.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | THIRD: The jurisdiction of organization/incorporation is |
| `entity.home_jurisdiction_name` | text | high | (name of foreign entity) |
| `entity.home_office_address_new.mailing` | text | high | (mailing address if different from above) |
| `entity.home_office_address_new.physical` | text | high | SECOND: The new home office address (physical location, not P.O. Box - street, city, state and zip code) |
| `entity.home_office_address_old` | text | high | FIRST: The old home office address as it appears on the record in the Secretary of State's office (street, city, state and zip code - old address) |
| `entity.maine_authorization_date` | text | high | and the date on which the entity was authorized to transact business in the State of Maine is |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |

_Showing 12 of 23 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_office_address_old is non-empty and contains a comma (street, city, state, zip pattern). (depends on `entity.home_office_address_old`)
- entity.home_office_address_new.physical is non-empty and does not begin with 'P.O.', 'PO Box', or 'Post Office Box' (form forbids P.O. boxes for the physical line). (depends on `entity.home_office_address_new.physical`)
- entity.home_office_address_old and entity.home_office_address_new.physical differ (the form's purpose is to record a change). (depends on `entity.home_office_address_old`, `entity.home_office_address_new.physical`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (this is a foreign-entity-only form). (depends on `entity.home_jurisdiction`)
- entity.maine_authorization_date is non-empty and not in the future. (depends on `entity.maine_authorization_date`)
- filing.signer.printed_name_and_capacity is non-empty (must be municipal official or postmaster per footnote 2). (depends on `filing.signer.printed_name_and_capacity`)
- filing.authorized_by is set to exactly one of {'town_municipality','us_postal_service'} (mutually exclusive checkboxes). (depends on `filing.authorized_by`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_office_address_old": "Sample Value",
    "home_office_address_new": {
      "physical": "Sample Value",
      "mailing": "Sample Value"
    },
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15"
  },
  "filing": {
    "authorized_by": "town_municipality",
    "date_signed": "2026-01-15"
  }
}
```
