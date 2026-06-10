# SKILL: Filling LLP_MLLP-2

**Form:** Application for Registration of Name (Foreign Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Register or renew the name of a foreign Limited Liability Partnership in Maine pursuant to 31 MRSA §806-A. Reserves the LLP's name in Maine for the calendar year and (per FIFTH) requires a certificate of existence dated within 90 days from the home jurisdiction. Does NOT authorize the LLP to transact business in Maine — that requires a separate Statement of Foreign Qualification.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.business_purpose` | text | high | FOURTH: A brief statement of the nature of the limited liability partnership's business: |
| `entity.formation_date_in_home_jurisdiction` | text | high | THIRD: The date of its organization is |
| `entity.home_jurisdiction` | text | high | SECOND: The state or country under the laws of which it is organized is |
| `entity.home_jurisdiction_name` | text | high | (Name of Foreign Limited Liability Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty (the foreign LLP's name as filed in its home jurisdiction). (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and not 'Maine' (the form is for foreign LLPs only). (depends on `entity.home_jurisdiction`)
- Exactly one of the FIRST checkboxes is selected (filing.application_type resolves to 'new' or 'renewal'). (depends on `filing.application_type`)
- entity.principal_office.physical_address is non-empty. (depends on `entity.principal_office.physical_address`)
- entity.formation_date_in_home_jurisdiction is on or before filing.date_signed. (depends on `entity.formation_date_in_home_jurisdiction`, `filing.date_signed`)
- entity.business_purpose is non-empty. (depends on `entity.business_purpose`)
- entity.certificate_of_existence_attached is true and dated within 90 days of filing.date_signed (FIFTH recital). (depends on `entity.certificate_of_existence_attached`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity includes both name and capacity (the signer must be a partner per 31 MRSA §806-A). (depends on `filing.signer.printed_name_and_capacity`)
- filing.entities[0].name matches entity.home_jurisdiction_name. (depends on `filing.entities[0].name`, `entity.home_jurisdiction_name`)
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
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    }
  }
}
```
