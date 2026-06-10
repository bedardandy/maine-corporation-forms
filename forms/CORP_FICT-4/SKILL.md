# SKILL: Filling CORP_FICT-4

**Form:** Statement of Intention to do Business under a Fictitious Name  
**Entity type:** Business Corporation  
**When to use:** Foreign-entity-only filing declaring intent to transact business in Maine under a fictitious name when the entity's real name is unavailable in Maine. Used by foreign corporations, LLCs, LPs, LLPs, and nonprofits.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | SECOND: Jurisdiction of incorporation/organization ___ and the date on which |
| `entity.home_jurisdiction_name` | text | high | (Exact Legal Name of Entity on the records of the Secretary of State) |
| `entity.maine_authorization_date` | text | high | the entity was authorized to transact business in Maine |
| `entity.maine_fictitious_name` | text | high | FIRST: The entity must transact business under the fictitious name of |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.maine_fictitious_name is non-empty. (depends on `entity.maine_fictitious_name`)
- entity.maine_fictitious_name differs from entity.home_jurisdiction_name (case-insensitive). (depends on `entity.maine_fictitious_name`, `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (this form is foreign-only). (depends on `entity.home_jurisdiction`)
- entity.maine_authorization_date is not in the future. (depends on `entity.maine_authorization_date`)
- filing.date_signed is on or after entity.maine_authorization_date (you can't file a fictitious-name statement before being authorized to transact business). (depends on `filing.date_signed`, `entity.maine_authorization_date`)
- filing.signer.title is non-empty (form's signature footnote restricts authorized signers per entity type). (depends on `filing.signer.title`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name": "Sample Value",
      "title": "Sample Value"
    },
    "entities": [
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
