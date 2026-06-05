# SKILL: Filling NP_MNPCA-11C

**Form:** Statement of Revocation of Voluntary Dissolution Proceedings (Domestic Nonprofit, Vote of Members or Directors)  
**Entity type:** Nonprofit Corporation  
**When to use:** Revoke previously authorized voluntary dissolution proceedings for a Maine domestic nonprofit corporation under 13-B MRSA §1102, based on a vote of the members (or directors when there are no voting members). Records the corporation's current officers (President, Treasurer, Secretary, Clerk) and up to three directors, indicates which body voted to revoke (SECOND), gives the Maine registered office address (THIRD), and is signed by an authorized officer; clerk/secretary certifies custody of the meeting minutes when the revocation was adopted by a member vote. Filing fee is $5. The resolution authorizing revocation must be attached as Exhibit A.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `director_1.address` | text | high | FIRST: Directors — Address (row 1) |
| `director_1.name` | text | high | FIRST: Directors — Name (row 1) |
| `director_2.address` | text | high | FIRST: Directors — Address (row 2) |
| `director_2.name` | text | high | FIRST: Directors — Name (row 2) |
| `director_3.address` | text | high | FIRST: Directors — Address (row 3) |
| `director_3.name` | text | high | FIRST: Directors — Name (row 3) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- All four required-role officer slots are populated: officer_president.name, officer_treasurer.name, officer_secretary.name, officer_clerk.name. (depends on `officer_president.name`, `officer_treasurer.name`, `officer_secretary.name`, `officer_clerk.name`)
- Every populated officer_<role>.name has a corresponding officer_<role>.address (and likewise for director_N). (depends on `officer_president.name`, `officer_president.address`, `officer_treasurer.name`, `officer_treasurer.address`, `officer_secretary.name`, `officer_secretary.address`, `officer_clerk.name`, `officer_clerk.address`, `director_1.name`, `director_1.address`, `director_2.name`, `director_2.address`, `director_3.name`, `director_3.address`)
- Exactly one of revocation.consent_class values is selected ('members' XOR 'directors_when_no_voting_members'). (depends on `revocation.consent_class`)
- registered_office.address_line2 (the wide labeled street/city/state/zip line) is non-empty. (depends on `registered_office.address_line2`)
- filing.signer_1.printed_name_and_capacity is non-empty (at least one authorized officer must sign per 13-B MRSA §104.1.B). (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- Form requires Exhibit A — the resolution adopted by the body identified in revocation.consent_class. Cannot be auto-validated against the AcroForm; rubric should note the requirement so that synth produces an exhibit reference and reviewers attach it at fill time. (depends on `revocation.consent_class`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "officer_president": {
    "name": "Sample Value",
    "address": "Sample Value"
  },
  "officer_treasurer": {
    "name": "Sample Value",
    "address": "Sample Value"
  },
  "officer_secretary": {
    "name": "Sample Value",
    "address": "Sample Value"
  },
  "officer_clerk": {
    "name": "Sample Value"
  }
}
```
