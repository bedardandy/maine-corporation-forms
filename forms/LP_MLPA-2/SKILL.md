# SKILL: Filling LP_MLPA-2

**Form:** Application for Registration of Name (Foreign Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Register or renew the name of a foreign limited partnership in Maine for the calendar year under 31 MRSA §1309.2. Name registration only reserves the right to use the name in Maine; it does not authorize the partnership to conduct business in Maine (page-1 footer). Renewable annually if filed between October 1 and December 31. Requires an attached certificate of existence dated within 90 days of delivery (FIFTH). LP analog of CORP_MBCA-2 and LLP_MLLP-2.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.business_purpose` | text | high | FOURTH: A brief statement of the nature of the limited partnership's business: |
| `entity.formation_date_in_home_jurisdiction` | text | high | THIRD: The date of its organization is |
| `entity.home_jurisdiction` | text | high | SECOND: The state or country under the laws of which it is organized is |
| `entity.home_jurisdiction_name` | text | high | (Name of Foreign Limited Partnership) |
| `entity.principal_office.physical_address.city_state_zip` | text | high | (street, city, state and zip code) |
| `entity.principal_office.physical_address.street` | text | high | SECOND: ...the address of its principal office is located at: (line 1) |
| `filing.application_type` | enum_select | high | FIRST: ('X' one box only.) This application is for a [ ] New |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |

_Showing 12 of 23 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- Exactly one of FIRST checkboxes is selected (filing.application_type ∈ {'new','renewal'}). (depends on `filing.application_type`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (foreign LPs only). (depends on `entity.home_jurisdiction`)
- entity.principal_office.physical_address.street and entity.principal_office.physical_address.city_state_zip are both non-empty. (depends on `entity.principal_office.physical_address.street`, `entity.principal_office.physical_address.city_state_zip`)
- entity.formation_date_in_home_jurisdiction is non-empty and on or before filing.date_signed. (depends on `entity.formation_date_in_home_jurisdiction`, `filing.date_signed`)
- entity.business_purpose is non-empty (FOURTH brief statement of the LP's business). (depends on `entity.business_purpose`)
- filing.signer.printed_name_and_capacity is non-empty (must be signed by a general partner per 31 MRSA §1324.1.M; capacity should reflect 'general partner' or equivalent). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- FIFTH paragraph requires an attached certificate of existence (or document of similar import) duly authenticated by the SOS of the home jurisdiction, dated within 90 days before delivery. Tracked as an attachment, not a form field. (depends on )

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
    "application_type": "new",
    "date_signed": "2026-01-15"
  }
}
```
