# SKILL: Filling CORP_ASUM-5

**Form:** Statement of Intention to Do Business Under an Assumed Name  
**Entity type:** Business Corporation  
**When to use:** Register an assumed name (DBA) for an existing Maine domestic or foreign-qualified entity (corporation, LLC, LP, LLP, nonprofit). Captures the entity's exact legal name, the assumed name, the location(s) where the assumed name will be used, and (for foreign entities only) jurisdiction of origin and Maine authorization date. Filing fee is entity-type-specific: $125 for-profit, $25 nonprofit (per page 0 header).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `assumed_name.additional_locations_exhibit` | text | high | Additional locations are attached hereto as Exhibit ___ and made a part hereof. |
| `assumed_name.locations` | text | high | SECOND: If the assumed name is not to be used at all the places of business in Maine, the location(s) where it will be used is (are): |
| `assumed_name.name` | text | high | FIRST: The entity intends to transact business under the assumed name of: |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | THIRD: (Foreign Entities Only) Jurisdiction of incorporation/organization |
| `entity.maine_authorization_date` | text | high | and the date on which the entity was authorized to transact business in Maine |
| `entity.name` | text | high | (Exact Legal Name of Entity on the records of the Secretary of State) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |

## Conditional logic

- entity.name is non-empty (must match SOS record exactly). (depends on `entity.name`)
- assumed_name.name is non-empty. (depends on `assumed_name.name`)
- assumed_name.name does not equal entity.name (an assumed name that matches the legal name is meaningless). (depends on `assumed_name.name`, `entity.name`)
- If assumed_name.additional_locations_exhibit is true, assumed_name.additional_locations_exhibit_letter must be non-empty. (depends on `assumed_name.additional_locations_exhibit`, `assumed_name.additional_locations_exhibit_letter`)
- entity.home_jurisdiction and entity.maine_authorization_date are either both populated (foreign entity) or both empty (domestic entity). (depends on `entity.home_jurisdiction`, `entity.maine_authorization_date`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.signer.printed_name and filing.signer.title are non-empty (Shape A). (depends on `filing.signer.printed_name`, `filing.signer.title`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15"
  },
  "assumed_name": {
    "name": "Sample Value",
    "locations": "Sample Value",
    "additional_locations_exhibit": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name": "Sample Value"
    }
  }
}
```
