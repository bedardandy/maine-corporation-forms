# SKILL: Filling LLC_MLLC-2

**Form:** Application for Registration of Name (Foreign Limited Liability Company)  
**Entity type:** Limited Liability Company  
**When to use:** Register or renew the name of a foreign Limited Liability Company in Maine for the calendar year under 31 MRSA §1511. Reserves the LLC's name in Maine but does NOT authorize the LLC to do business in Maine — that requires a separate Statement of Foreign Qualification (LLC_MLLC-12). Renewable annually if filed between October 1 and December 31. Per FIFTH, requires a certificate of existence dated within 90 days from the home jurisdiction (no AcroForm widget — manual attachment).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.business_purpose` | text | high | FOURTH: A brief statement of the nature of the limited liability company's business: |
| `entity.formation_date_in_home_jurisdiction` | text | high | THIRD: The date of its organization is |
| `entity.home_jurisdiction` | text | high | SECOND: The state or other jurisdiction under the laws of which it is organized is |
| `entity.home_jurisdiction_name` | text | high | (Name of Foreign Limited Liability Company) |
| `entity.principal_office.physical_address` | text | high | and the address of its principal office is located at: (line 1) (fills multiple widgets) |
| `filing.application_type` | enum_select | high | FIRST: ('X' one box only.) This application is for a [ ] new |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |

_Showing 12 of 22 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- Exactly one of the FIRST checkboxes is selected (filing.application_type ∈ {'new','renewal'}). (depends on `filing.application_type`)
- entity.home_jurisdiction is non-empty and not 'Maine' or 'ME' (the form is for foreign LLCs only). (depends on `entity.home_jurisdiction`)
- entity.principal_office.physical_address is non-empty. (depends on `entity.principal_office.physical_address`)
- entity.formation_date_in_home_jurisdiction is non-empty and on or before filing.date_signed. (depends on `entity.formation_date_in_home_jurisdiction`, `filing.date_signed`)
- entity.business_purpose is non-empty. (depends on `entity.business_purpose`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.entities[0].name equals entity.home_jurisdiction_name. (depends on `filing.entities[0].name`, `entity.home_jurisdiction_name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "principal_office": {
      "physical_address": "Sample Value"
    },
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "business_purpose": "Sample Value"
  },
  "filing": {
    "application_type": "new",
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
