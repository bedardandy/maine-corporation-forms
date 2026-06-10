# SKILL: Filling LP_MLPA-10

**Form:** Articles of Merger (Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** File Articles of Merger relating to a Limited Partnership under 31 MRSA §1438. Records the constituent (party) organizations, the surviving organization (name, form, jurisdiction), THIRD declaration that the survivor was created by the merger, FOURTH effective date, FIFTH election (created-by-merger vs. preexisted, with sub-options for org-doc amendments), SEVENTH service-of-process address for foreign survivors, EIGHTH additional-info exhibit, and per-party signature blocks (4 inline + copy-page overflow). For preexisting LP constituents, §1438 footnote requires signature by ALL general partners listed in the LP's Certificate of Limited Partnership.

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
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

_Showing 12 of 46 canonical keys — the full set is in mapping.json._

## Conditional logic

- merger.parties[0].recital and merger.parties[1].recital are both non-empty (a merger requires at least 2 constituent parties). (depends on `merger.parties[0].recital`, `merger.parties[1].recital`)
- If all four merger.parties[N].recital are populated AND any further parties exist beyond row 4, merger.additional_parties_attached must be true and merger.additional_parties_exhibit_letter must be set. (depends on `merger.parties[3].recital`, `merger.additional_parties_attached`, `merger.additional_parties_exhibit_letter`)
- merger.surviving_entity.name, merger.surviving_entity.form, and merger.surviving_entity.jurisdiction are all non-empty. (depends on `merger.surviving_entity.name`, `merger.surviving_entity.form`, `merger.surviving_entity.jurisdiction`)
- merger.effective_date is non-empty. (depends on `merger.effective_date`)
- Exactly one merger.fifth_election option is selected. (depends on `merger.fifth_election`)
- If merger.fifth_election='preexisted', exactly one merger.fifth_subelection option must be selected (amendments_attached vs organizational_docs_unchanged). (depends on `merger.fifth_election`, `merger.fifth_subelection`)
- merger.surviving_entity_created_by_merger=true iff merger.fifth_election='created_by_merger' (THIRD and FIFTH option 1 declare the same fact). (depends on `merger.surviving_entity_created_by_merger`, `merger.fifth_election`)
- If merger.surviving_entity.jurisdiction is not 'Maine'/'ME', merger.foreign_survivor.service_of_process_physical_address must be set. (depends on `merger.surviving_entity.jurisdiction`, `merger.foreign_survivor.service_of_process_physical_address`)
- For each populated merger.parties[N].recital (N in 0..3), the corresponding signature_block.name_and_type, signature_block.date_signed, and signature_block.signer_1.printed_name_and_capacity must be non-empty. (depends on `merger.parties[0].recital`, `merger.parties[0].signature_block.name_and_type`, `merger.parties[0].signature_block.date_signed`, `merger.parties[0].signature_block.signer_1.printed_name_and_capacity`)
- filing.contact and signature dates not in the future (effective_date may be future-dated; signature dates may not). (depends on `merger.parties[0].signature_block.date_signed`)
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
