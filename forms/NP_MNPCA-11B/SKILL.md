# SKILL: Filling NP_MNPCA-11B

**Form:** Statement of Revocation of Voluntary Dissolution Proceedings (Nonprofit)  
**Entity type:** Nonprofit Corporation  
**When to use:** Revoke previously authorized voluntary dissolution proceedings for a Maine domestic nonprofit corporation under 13-B MRSA §1102. Recites current officers (President, Treasurer, Secretary, Clerk) and up to three directors, identifies the consent source (members vs directors, with written consent attached as Exhibit A), and states the corporation's Maine registered office. Signed by an authorized officer; if consent is by members, the clerk/secretary attests minutes custody.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- At least one officer (officer_1) is fully populated. President is the conventional row-1 occupant. (depends on `officer_1.printed_name`, `officer_1.address`)
- For each officer_N row that is populated, both .printed_name and .address are non-empty (no half-filled rows). (depends on `officer_1.printed_name`, `officer_1.address`, `officer_2.printed_name`, `officer_2.address`)
- Exactly one of SECOND members/directors checkboxes is selected. (depends on `revocation.consent_source`)
- registered_agent.physical_address is non-empty. (depends on `registered_agent.physical_address`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- At least one of filing.signer or filing.signer_2 is fully populated. Form footnote requires 'any authorized officer' to sign — singular, so one slot is sufficient. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_2.printed_name_and_capacity`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "officer_1": {
    "printed_name": "Sample Value",
    "address": "Sample Value"
  },
  "officer_2": {
    "printed_name": "Sample Value",
    "address": "Sample Value"
  },
  "officer_3": {
    "printed_name": "Sample Value",
    "address": "Sample Value"
  },
  "officer_4": {
    "printed_name": "Sample Value"
  }
}
```
