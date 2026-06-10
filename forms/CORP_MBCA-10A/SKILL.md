# SKILL: Filling CORP_MBCA-10A

**Form:** Statement of Abandonment of Merger or Share Exchange  
**Entity type:** Business Corporation  
**When to use:** Abandon a previously filed Articles of Merger or Share Exchange (MBCA-10) before it becomes effective, pursuant to 13-C MRSA §1108.2. The form identifies the party filing the abandonment, lists up to four parties to the original transaction, and is signed by a single authorized representative (Shape D — combined name+capacity).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of party to the merger or share exchange filing this document) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED ____ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity(s) on the submitted filings [2] |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the specific party filing the abandonment) is non-empty. (depends on `entity.name`)
- merger.parties[0].recital and merger.parties[1].recital are both non-empty (a merger by definition has at least 2 constituent parties; the abandonment recital must list them). (depends on `merger.parties[0].recital`, `merger.parties[1].recital`)
- entity.name appears as a substring of at least one merger.parties[N].recital — the filer must be one of the parties to the merger per 13-C §1108.2. (depends on `entity.name`, `merger.parties[0].recital`, `merger.parties[1].recital`, `merger.parties[2].recital`, `merger.parties[3].recital`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.entities[0].name equals entity.name (the party filing the abandonment). (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "merger": {
    "parties": [
      {
        "recital": "Sample Value"
      },
      {
        "recital": "Sample Value"
      },
      {
        "recital": "Sample Value"
      },
      {
        "recital": "Sample Value"
      }
    ]
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities": [
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
