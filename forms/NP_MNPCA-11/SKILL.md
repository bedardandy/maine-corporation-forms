# SKILL: Filling NP_MNPCA-11

**Form:** Statement of Intent to Dissolve (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** File a Statement of Intent to Dissolve a Maine domestic nonprofit corporation under 13-B MRSA §1101 by written consent (members or, if no voting members, directors). Recites the names and addresses of the corporation's current officers (President, Treasurer, Secretary, Clerk) and up to three directors, indicates which class executed the written consent (SECOND), references Articles of Dissolution (THIRD), gives the Maine registered office address (FOURTH), and is signed by any authorized officer. When the consent is by member vote, a clerk/secretary certifies custody of the minutes.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `certification.clerk_signature_printed_name` | text | high | MUST BE COMPLETED FOR VOTE OF MEMBERS — (signature of clerk, secretary or asst. secretary) |
| `director_1.address` | text | high | FIRST: Directors — Address (row 1) |
| `director_1.name` | text | high | FIRST: Directors — Name (row 1) |
| `director_2.address` | text | high | FIRST: Directors — Address (row 2) |
| `director_2.name` | text | high | FIRST: Directors — Name (row 2) |
| `director_3.address` | text | high | FIRST: Directors — Address (row 3) |
| `director_3.name` | text | high | FIRST: Directors — Name (row 3) |
| `dissolution.consent_class` | text | high | SECOND: All members of the corporation entitled to vote (fills multiple widgets) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of dissolution.consent_class values is selected ('members' XOR 'directors_when_no_voting_members'). (depends on `dissolution.consent_class`)
- All four required-role officer slots are populated: officer_president.name, officer_treasurer.name, officer_secretary.name, officer_clerk.name (the FIRST table reserves a fixed slot for each role per 13-B MRSA §704). (depends on `officer_president.name`, `officer_treasurer.name`, `officer_secretary.name`, `officer_clerk.name`)
- Every populated officer_<role>.name has a corresponding officer_<role>.address (and likewise for director_N). (depends on `officer_president.name`, `officer_president.address`, `officer_treasurer.name`, `officer_treasurer.address`, `officer_secretary.name`, `officer_secretary.address`, `officer_clerk.name`, `officer_clerk.address`, `director_1.name`, `director_1.address`, `director_2.name`, `director_2.address`, `director_3.name`, `director_3.address`)
- registered_office.address_line2 (the wide labeled line) is non-empty. (depends on `registered_office.address_line2`)
- filing.signer_1.printed_name_and_capacity is non-empty (at least one authorized officer must sign per 13-B MRSA §104.1.B). (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- If dissolution.consent_class='members', certification.clerk_signature_printed_name must be non-empty. If consent_class='directors_when_no_voting_members', the clerk certification is not required. (depends on `dissolution.consent_class`, `certification.clerk_signature_printed_name`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

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
