# SKILL: Filling NP_MNPCA-2

**Form:** Application for Registration of Name (Foreign Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Register or renew the corporate name of a foreign nonprofit corporation in Maine under 13-B MRSA §303-A. A registration secures the name for the calendar year of filing; renewal must be filed between October 1 and December 31. Requires an attached certificate of existence (or document of similar import) authenticated by the home jurisdiction within 90 days before delivery.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | THIRD: The date of its incorporation is ____ |
| `entity.home_jurisdiction` | text | high | SECOND: The state or country under the laws of which it is incorporated is ____ |
| `entity.home_jurisdiction_name` | text | high | (Name of foreign corporation) |
| `entity.maine_business_purpose` | text | high | FOURTH: A brief statement of the nature of the corporation's activities to be conducted in Maine. |
| `entity.principal_office.address_line1` | text | high | SECOND: ...and the address of its principal office is located at: ____ (line 1) |
| `entity.principal_office.address_line2` | text | high | SECOND: ____ (street, city, state and zip code) (line 2) |
| `filing.application_type` | text | high | FIRST: ('X' one box only.) [ ] new (fills multiple widgets) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- Exactly one of FIRST options is selected (filing.application_type ∈ {'new', 'renewal'}). (depends on `filing.application_type`)
- entity.home_jurisdiction is non-empty. (depends on `entity.home_jurisdiction`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (this is a foreign-only form). (depends on `entity.home_jurisdiction`)
- entity.principal_office.address_line2 (the wide labeled street/city/state/zip line) is non-empty. (depends on `entity.principal_office.address_line2`)
- entity.formation_date_in_home_jurisdiction is non-empty. (depends on `entity.formation_date_in_home_jurisdiction`)
- entity.maine_business_purpose is non-empty (FOURTH paragraph). (depends on `entity.maine_business_purpose`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- If filing.application_type='renewal', filing.date_signed is between October 1 and December 31 (page-0 instruction: 'A renewal application can be filed between October 1 and December 31 of the current calendar year'). (depends on `filing.application_type`, `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "principal_office": {
      "address_line1": "Sample Value",
      "address_line2": "Sample Value"
    },
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "maine_business_purpose": "Sample Value"
  },
  "filing": {
    "application_type": "Sample Value",
    "date_signed": "2026-01-15"
  }
}
```
