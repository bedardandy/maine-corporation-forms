# SKILL: Filling NP_MNPCA-10

**Form:** Articles of Merger (Maine/Maine Domestic Nonprofit)  
**Entity type:** Nonprofit Corporation  
**When to use:** File Articles of Merger between two Maine domestic nonprofit corporations under 13-B MRSA §904 (or 13 MRSA §961 for older filings). Records the merging-corp(s) and surviving corp, public-vs-mutual benefit classification, plan-of-merger exhibit, per-corporation voting recital (4 mutually-exclusive options each), registered-office addresses for both, optional future effective date, and dual signature blocks with member-vote certifications.

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

_Showing 12 of 36 canonical keys — the full set is in mapping.json._

## Conditional logic

- merger.merging_corporations_recital is non-empty. (depends on `merger.merging_corporations_recital`)
- merger.surviving_corporation_name is non-empty. (depends on `merger.surviving_corporation_name`)
- Each populated merger.parties[N] has exactly one vote_method selected. Two parties expected inline (block 1 and block 2 on page 0); additional parties go on attached exhibits. (depends on `merger.parties[0].vote_method`, `merger.parties[1].vote_method`)
- If merger.parties[N].vote_method is set (any value), merger.parties[N].vote_method_date should be set (each option references a date — meeting/consent/board-meeting). (depends on `merger.parties[0].vote_method`, `merger.parties[0].vote_method_date`, `merger.parties[1].vote_method`, `merger.parties[1].vote_method_date`)
- Both merger.surviving_corp.registered_office_address and merger.merging_corp.registered_office_address are non-empty. (depends on `merger.surviving_corp.registered_office_address_line2`, `merger.merging_corp.registered_office_address_line2`)
- If merger.future_effective_date is set, it must be on or after filing.date_signed AND no later than filing.date_signed + 60 days (per 13-B MRSA cap noted on form). (depends on `merger.future_effective_date`)
- If merger.parties[N].vote_method is one of {'majority_member_vote', 'supermajority_member_vote', 'written_consent_of_members'}, the corresponding clerk_certification block must be populated (corporation_name + signer). Not required when vote_method='board_of_directors_majority_vote'. (depends on `merger.parties[0].vote_method`, `merger.parties[0].clerk_certification.signer_printed_name_and_title`)

## Example case data

```json
{
  "merger": {
    "merging_corporations_recital": "Sample Value",
    "surviving_corporation_name": "Sample Value",
    "plan_exhibit_letter": "Sample Value",
    "parties": [
      {
        "name": "Sample Value",
        "vote_method": "Sample Value",
        "vote_method_date": "2026-01-15"
      },
      {
        "name": "Sample Value",
        "vote_method": "Sample Value"
      }
    ]
  }
}
```
