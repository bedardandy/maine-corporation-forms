# SKILL: Filling CORP_MBCA-19B

**Form:** Statement of Abandonment of Domestication (Domestic or Foreign Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Abandon a pending domestication of a business corporation under 13-C MRSA §926. The form has two mutually-exclusive paths: (1) Domestic Business — abandons a charter-surrender filing (CORP_MBCA-19A) before its effective date, keeping the corporation's Maine domestic status; (2) Foreign Business — abandons an articles-of-domestication filing (CORP_MBCA-19) before it has become effective, keeping the corporation as foreign. Both paths require an officer's signature and result in the underlying domestication being treated as if never filed.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `abandonment.path` | enum_select | high | FIRST: [ ] (Domestic Business) The domestication is abandoned after articles of charter surrender have been filed in accordance with the laws of the foreign jurisdiction after articles of domestication have been filed with the Secretary of State but before the domestication has become effective on ___. |
| `abandonment.would_be_effective_date` | text | high | ...but before the domestication has become effective on ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 19 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of FIRST checkboxes is selected (abandonment.path ∈ {'domestic', 'foreign'}). (depends on `abandonment.path`)
- If abandonment.path='domestic', abandonment.would_be_effective_date must be non-empty (the form's only fillable date in the FIRST domestic recital). (depends on `abandonment.path`, `abandonment.would_be_effective_date`)
- If abandonment.would_be_effective_date is set, it must be on or after filing.date_signed (the abandonment is filed BEFORE the domestication would have become effective per §926). (depends on `abandonment.would_be_effective_date`, `filing.date_signed`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (must be an officer or duly authorized representative per §926). (depends on `filing.signer.printed_name_and_capacity`)
- filing.entities[0].name equals entity.name (the corporation's name on this filing). (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "abandonment": {
    "path": "domestic",
    "would_be_effective_date": "2026-01-15"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "expedited_service": {},
    "entities": [
      {
        "name": "Sample Value"
      },
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
