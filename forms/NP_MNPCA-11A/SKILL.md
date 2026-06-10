# SKILL: Filling NP_MNPCA-11A

**Form:** Statement of Intent to Dissolve (Domestic Nonprofit Corporation, Vote of Members or Directors)  
**Entity type:** Nonprofit Corporation  
**When to use:** File a Statement of Intent to Dissolve a Maine domestic nonprofit corporation under 13-B MRSA §1101 by *vote* (rather than written consent — written-consent variant is NP_MNPCA-11). Recites the names and addresses of the corporation's current officers (President, Treasurer, Secretary, Clerk) and up to three directors, indicates which body adopted the resolution (members vs directors when no voting members), records vote tallies (THIRD), gives the Maine registered office address (FIFTH), and is signed by an authorized officer; clerk/secretary certifies custody of the meeting minutes when the resolution was adopted by a member vote. Filing fee is $10. This filing is preliminary — Articles of Dissolution (Form MNPCA-11D or 11E) must follow.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `director_1.address` | text | high | FIRST: Directors — Address (row 1) |
| `director_1.name` | text | high | FIRST: Directors — Name (row 1) |
| `director_2.address` | text | high | FIRST: Directors — Address (row 2) |
| `director_2.name` | text | high | FIRST: Directors — Name (row 2) |
| `director_3.address` | text | high | FIRST: Directors — Address (row 3) |
| `director_3.name` | text | high | FIRST: Directors — Name (row 3) |
| `dissolution.consent_class` | text | high | SECOND: ('X' one box only) Exhibit A attached hereto is a copy of the resolution adopted by: The members of the corporation entitled to vote. (fills multiple widgets) |
| `dissolution.total_voters` | text | high | THIRD: Number of Members/Directors and Entitled to Vote (wide blank below column header, y≈541-562) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |

_Showing 12 of 38 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- All four required-role officer slots are populated: officer_president.name, officer_treasurer.name, officer_secretary.name, officer_clerk.name (FIRST table reserves a fixed slot for each role per 13-B MRSA §704). (depends on `officer_president.name`, `officer_treasurer.name`, `officer_secretary.name`, `officer_clerk.name`)
- Every populated officer_<role>.name has a corresponding officer_<role>.address (and likewise for director_N). (depends on `officer_president.name`, `officer_president.address`, `officer_treasurer.name`, `officer_treasurer.address`, `officer_secretary.name`, `officer_secretary.address`, `officer_clerk.name`, `officer_clerk.address`, `director_1.name`, `director_1.address`, `director_2.name`, `director_2.address`, `director_3.name`, `director_3.address`)
- Exactly one of dissolution.consent_class values is selected ('members' XOR 'directors_when_no_voting_members'). (depends on `dissolution.consent_class`)
- dissolution.total_voters and at least one of dissolution.votes_for/votes_for_total are populated. dissolution.votes_against may be 0 but the field should be reachable. (depends on `dissolution.total_voters`, `dissolution.votes_for`, `dissolution.votes_for_total`)
- registered_office.address_line2 (the wide labeled street/city/state/zip line) is non-empty. (depends on `registered_office.address_line2`)
- filing.signer_1.printed_name_and_capacity is non-empty (at least one authorized officer must sign per 13-B MRSA §104.1.B). (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- If dissolution.consent_class='members', certification.clerk_signature_printed_name must be non-empty. If consent_class='directors_when_no_voting_members', the clerk certification is not required. (depends on `dissolution.consent_class`, `certification.clerk_signature_printed_name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "officer_president": {
    "name": "Sample Value"
  },
  "officer_treasurer": {
    "name": "Sample Value"
  },
  "officer_secretary": {
    "name": "Sample Value"
  },
  "officer_clerk": {
    "name": "Sample Value"
  },
  "director_1": {
    "name": "Sample Value"
  },
  "director_2": {
    "name": "Sample Value"
  },
  "director_3": {
    "name": "Sample Value"
  }
}
```
