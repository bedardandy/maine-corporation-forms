# SKILL: Filling LLC_MLLC-10

**Form:** Statement of Merger (Relating to a Limited Liability Company)  
**Entity type:** Limited Liability Company  
**When to use:** File a Statement of Merger involving at least one Maine LLC under 31 MRSA §1641. Records the constituent (party) organizations to the merger, the surviving organization (name, form, jurisdiction, date of organization, principal office), the THIRD-paragraph election (survivor created by this merger vs. preexisted, with sub-options for organizational-document amendments), the effective date, the foreign-survivor service-of-process address (SIXTH), an additional-information exhibit (SEVENTH), and per-party signature blocks (4 inline + copy-page overflow). Per 31 MRSA §§1643.1 / 1676.1, the statement must be signed by an authorized representative of each constituent organization.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity(s) on the submitted filings [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

_Showing 12 of 47 canonical keys — the full set is in mapping.json._

## Conditional logic

- merger.parties[0].recital and merger.parties[1].recital are both non-empty (a merger requires at least 2 constituent organizations). (depends on `merger.parties[0].recital`, `merger.parties[1].recital`)
- If all four merger.parties[N].recital are populated AND further parties exist, merger.additional_parties_attached must be true and merger.additional_parties_exhibit_letter must be set. (depends on `merger.parties[3].recital`, `merger.additional_parties_attached`, `merger.additional_parties_exhibit_letter`)
- merger.surviving_entity.name, merger.surviving_entity.form, merger.surviving_entity.jurisdiction, merger.surviving_entity.date_of_organization, and merger.surviving_entity.principal_office.physical_address are all non-empty. (depends on `merger.surviving_entity.name`, `merger.surviving_entity.form`, `merger.surviving_entity.jurisdiction`, `merger.surviving_entity.date_of_organization`, `merger.surviving_entity.principal_office.physical_address`)
- Exactly one merger.third_election option is selected ('created_by_merger' or 'preexisted'). (depends on `merger.third_election`)
- If merger.third_election='preexisted', exactly one merger.third_subelection option must be selected (amendments_attached vs organizational_docs_unchanged). If merger.third_election='created_by_merger', merger.third_subelection must be unset. (depends on `merger.third_election`, `merger.third_subelection`)
- merger.effective_date is non-empty. (depends on `merger.effective_date`)
- If merger.surviving_entity.jurisdiction is not 'Maine'/'ME', merger.foreign_survivor.service_of_process_physical_address must be set. (depends on `merger.surviving_entity.jurisdiction`, `merger.foreign_survivor.service_of_process_physical_address`)
- For each populated merger.parties[N].recital (N in 0..3), the corresponding signature_block.name_and_type, signature_block.date_signed, and signature_block.signer_1.printed_name_and_capacity must be non-empty. (depends on `merger.parties[0].recital`, `merger.parties[0].signature_block.name_and_type`, `merger.parties[0].signature_block.date_signed`, `merger.parties[0].signature_block.signer_1.printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

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
      "name": "Sample Value",
      "form": "Sample Value"
    }
  }
}
```
