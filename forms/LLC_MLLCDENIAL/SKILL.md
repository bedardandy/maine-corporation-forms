# SKILL: Filling LLC_MLLCDENIAL

**Form:** Statement of Denial of Authority (Maine LLC)  
**Entity type:** Limited Liability Company  
**When to use:** File a Statement of Denial of Authority for a Maine limited liability company under 31 MRSA §1543. The signer denies the authority that a previously filed Statement of Authority granted them — either by name (as an authorized person) or by virtue of holding a position the prior statement named. Under §1543, the denial operates as a limitation cancelling the granted authority. Per §1676.1.D, the denial must be signed by the person who is denying. The signer must furnish a copy of the denial to the LLC.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `denial.original_statement_filing_date` | text | high | Pursuant to 31 MRSA §1543, the undersigned hereby denies the statement of authority originally filed on ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Limited Liability Company) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 18 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- denial.original_statement_filing_date is non-empty (SOS needs this to locate the original record). (depends on `denial.original_statement_filing_date`)
- denial.original_statement_filing_date is on or before filing.date_signed (cannot deny a statement that has not yet been filed). (depends on `denial.original_statement_filing_date`, `filing.date_signed`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D; per §1676.1.D the signer must be the person whose authority is being denied). (depends on `filing.signer.printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, LLC"
  },
  "denial": {
    "original_statement_filing_date": "2026-01-15"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    },
    "expedited_service": {},
    "total_fees_dollars": "Sample Value"
  }
}
```
