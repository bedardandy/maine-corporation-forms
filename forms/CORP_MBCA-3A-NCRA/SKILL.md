# SKILL: Filling CORP_MBCA-3A-NCRA

**Form:** Statement of Resignation of Noncommercial Clerk (Domestic Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** File a statement of resignation by the noncommercial clerk currently appearing on the Maine SOS record for a Maine domestic business corporation, pursuant to 5 MRSA §111. The clerk attests to their identity and address as on record (FIRST), names a corporate officer to whom the SOS-required notice of resignation will be sent (SECOND), dates and signs the statement. The clerk's appointment terminates 31 days after this filing is delivered to the corporation. Filing fee is $35 per the page-0 header. 2 pages, 22 widgets. Domestic-BC sibling of CORP_MBCA-12E-NCRA (foreign-BC variant) and LLC_MLLC-3A-NCRA — identical body structure, differs only in entity-type heading. 'Clerk' here is the legacy 13-C MRSA term for what newer entity statutes call 'registered agent'; canonical keys reuse the registered_agent.* namespace per the MBCA-12E-NCRA / MLLC-3A-NCRA precedent so synth/rubric authors do not have to disambiguate clerk vs RA.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Corporation as it appears on the records of the Secretary of State) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |

_Showing 12 of 22 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty (must match SOS record). (depends on `entity.name`)
- registered_agent.name is non-empty (the resigning clerk's name as on record). (depends on `registered_agent.name`)
- registered_agent.physical_address is non-empty (must match SOS record verbatim). (depends on `registered_agent.physical_address`)
- resignation_notice.recipient_name is non-empty. (depends on `resignation_notice.recipient_name`)
- resignation_notice.recipient_address is non-empty. (depends on `resignation_notice.recipient_address`)
- resignation_notice.recipient_title is non-empty (must be a corporate-officer title — President, Treasurer, Secretary, etc.). (depends on `resignation_notice.recipient_title`)
- filing.date_signed is non-empty and not in the future (resignation effective date is filing.date_signed + 31 days, by §111). (depends on `filing.date_signed`)
- filing.signer.printed_name is non-empty. (depends on `filing.signer.printed_name`)
- filing.signer.printed_name should match registered_agent.name (the resigning clerk is the signer; mismatch indicates either a typo or that someone other than the clerk of record is signing, which §111 does not authorize). (depends on `filing.signer.printed_name`, `registered_agent.name`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "registered_agent": {
    "name": "Sample Value",
    "physical_address": "Sample Value"
  },
  "resignation_notice": {
    "recipient_name": "Sample Value",
    "recipient_address": "Sample Value",
    "recipient_title": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name": "Sample Value"
    }
  }
}
```
