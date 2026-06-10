# SKILL: Filling CORP_MBCA-2

**Form:** Application for Registration of Name (Foreign Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Register or renew the name of a foreign business corporation in Maine for the calendar year under 13-C MRSA §403. Name registration only reserves the right to use the name in Maine; it does not authorize the corporation to conduct business in Maine (which requires a separate Statement of Foreign Qualification, MBCA-12). Renewable annually if filed between October 1 and December 31.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.business_purpose` | text | high | FOURTH: A brief statement of the nature of the corporation's business: |
| `entity.formation_date_in_home_jurisdiction` | text | high | THIRD: The date of its incorporation is |
| `entity.home_jurisdiction` | text | high | SECOND: The state or country under the laws of which it is incorporated is |
| `entity.home_jurisdiction_name` | text | high | (Name of Foreign Corporation) |
| `entity.principal_office.physical_address.city_state_zip` | text | high | (street, city, state and zip code) |
| `entity.principal_office.physical_address.street` | text | high | SECOND: ...the address of its principal office is located at: (line 1) |
| `filing.application_type` | text | high | FIRST: ('X' one box only.) This application is for a [ ] new ... registration of corporate name (fills multiple widgets) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |

_Showing 12 of 23 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- Exactly one of FIRST checkboxes is selected (filing.application_type ∈ {'new','renewal'}). (depends on `filing.application_type`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (foreign corporations only — a domestic Maine corp would file MBCA-5 / amend instead). (depends on `entity.home_jurisdiction`)
- entity.principal_office.physical_address.street and entity.principal_office.physical_address.city_state_zip are both non-empty. (depends on `entity.principal_office.physical_address.street`, `entity.principal_office.physical_address.city_state_zip`)
- entity.formation_date_in_home_jurisdiction is non-empty. (depends on `entity.formation_date_in_home_jurisdiction`)
- entity.business_purpose is non-empty. (depends on `entity.business_purpose`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- FIFTH paragraph requires an attached certificate of existence (or document of similar import) duly authenticated by the SOS of the home jurisdiction, dated within 90 days before delivery. Not enforceable from form fields alone — tracked manually as filing.notes. (depends on )

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "principal_office": {
      "physical_address": {
        "street": "Sample Value",
        "city_state_zip": "Sample Value"
      }
    },
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "business_purpose": "Sample Value"
  },
  "filing": {
    "application_type": "Sample Value",
    "date_signed": "2026-01-15"
  }
}
```
