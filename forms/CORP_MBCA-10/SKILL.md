# SKILL: Filling CORP_MBCA-10

**Form:** Articles of Merger or Share Exchange (Survivor is a Corporation)  
**Entity type:** Business Corporation  
**When to use:** File Articles of Merger or Share Exchange under 13-C MRSA §1106 when the surviving/acquiring entity is a Maine business corporation. Records the multi-party recital, surviving entity, principal place of business, exhibit attachments for amendments or new-corporation provisions, future effective date, shareholder/foreign-authorization elections, foreign survivor service-of-process address, and per-party signature blocks (up to 3 inline + copy-page overflow).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |
| `merger.additional_parties_attached` | text | high | Names, type of entity, jurisdiction and effective date of the additional parties to the merger or share exchange are attached as Exhibit ___, and made a part hereof. |

_Showing 12 of 45 canonical keys — the full set is in mapping.json._

## Conditional logic

- merger.parties[] has at least 2 entries (a merger requires at least 2 constituent parties). (depends on `merger.parties[0].recital`, `merger.parties[1].recital`)
- If merger.parties[] exceeds 4, merger.additional_parties_attached must be true and merger.additional_parties_exhibit_letter must be set. (depends on `merger.parties[0].recital`, `merger.parties[1].recital`, `merger.parties[2].recital`, `merger.parties[3].recital`, `merger.additional_parties_attached`, `merger.additional_parties_exhibit_letter`)
- merger.surviving_entity.name_and_jurisdiction is non-empty. (depends on `merger.surviving_entity.name_and_jurisdiction`)
- merger.surviving_entity.principal_office.physical_address is non-empty. (depends on `merger.surviving_entity.principal_office.physical_address`)
- Exactly one of merger.fourth_election options is selected (FOURTH says 'X one box only'). (depends on `merger.fourth_election`)
- If merger.fourth_election='survivor_originating_doc_amended', merger.survivor_amendments_exhibit_letter must be set. If merger.fourth_election='new_corporation_created', merger.new_corporation_provisions_exhibit_letter must be set. (depends on `merger.fourth_election`, `merger.survivor_amendments_exhibit_letter`, `merger.new_corporation_provisions_exhibit_letter`)
- Exactly one of merger.sixth_election options is selected. (depends on `merger.sixth_election`)
- If any merger.parties[N].recital indicates a foreign jurisdiction (not Maine/ME), one of merger.seventh_election options must be selected and merger.foreign_survivor.service_of_process_mailing_address must be set when the survivor is foreign. (depends on `merger.parties[0].recital`, `merger.parties[1].recital`, `merger.seventh_election`, `merger.foreign_survivor.service_of_process_mailing_address`)
- If merger.future_effective_date is set, it must be on or after filing.date_signed. (depends on `merger.future_effective_date`, `filing.date_signed`)
- For each populated merger.parties[N].recital with N<3, the corresponding signature block must have name_and_type, date_signed, and at least signer_1 populated. (depends on `merger.parties[0].signature_block.name_and_type`, `merger.parties[0].signature_block.date_signed`, `merger.parties[0].signature_block.signer_1.printed_name_and_capacity`)

## Example case data

```json
{
  "merger": {
    "parties[0]": {
      "recital": "Sample Value"
    },
    "parties[1]": {
      "recital": "Sample Value"
    },
    "parties[2]": {
      "recital": "Sample Value"
    },
    "parties[3]": {
      "recital": "Sample Value"
    },
    "additional_parties_attached": "Sample Value",
    "additional_parties_exhibit_letter": "Sample Value",
    "surviving_entity": {
      "name_and_jurisdiction": "Sample Value",
      "principal_office": {
        "physical_address": "Sample Value"
      }
    }
  }
}
```
