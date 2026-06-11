# SKILL: Filling NP_MNPCA-6A_0

**Form:** Restated Articles of Incorporation (Domestic Nonprofit Corporation, alternate template)  
**Entity type:** Nonprofit Corporation  
**When to use:** File Restated Articles of Incorporation for an existing Maine domestic nonprofit corporation under 13-B MRSA §805. The full restated text MUST be attached as an exhibit (typically the contents of Form MNPCA-6-1, which the form footnote requires accompany this filing). The form records the adoption date and the adoption method (one of: members-at-meeting majority, members-at-meeting supermajority per articles, written consent of all entitled members, or board majority vote when there are no entitled members). It also captures the (possibly new) registered agent. This is the alternate template variant — uses a 'Filer Contact Cover Letter' (page 2) with C1-C12 widget naming and an additional 'List type of filing(s) enclosed' free-text block not present in the standard cover-letter primitive.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.name` | text | high | (Name of Corporation as it appears on the records of the Secretary of State) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested recipient) |
| `filing.contact.email` | text | high | (Email address) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | Dated |
| `filing.enclosed_filing_types.line1` | text | high | List type of filing(s) enclosed (i.e. Articles of Incorporation, Articles of Merger, ...) [line 1] |
| `filing.enclosed_filing_types.line2` | text | high | List type of filing(s) enclosed [line 2] |
| `filing.entities[0].name` | text | high | Name of Entity (s) [line 1] |

_Showing 12 of 25 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- restatement.text_exhibit_letter is non-empty (the form footnote requires Form MNPCA-6-1 with the full restated text accompany this filing). (depends on `restatement.text_exhibit_letter`)
- restatement.adoption_date is non-empty and parses as a date on or before filing.date_signed. (depends on `restatement.adoption_date`, `filing.date_signed`)
- Exactly one of Check Box4/5/6/8 is selected (restatement.adoption_method set to a single enum value). (depends on `restatement.adoption_method`)
- Exactly one of Commercial or Noncommercial Registered Agent is selected. (depends on `registered_agent.type`)
- registered_agent.name is non-empty. (depends on `registered_agent.name`)
- registered_agent.physical_address is non-empty and is not a P.O. Box. (depends on `registered_agent.physical_address`)
- If registered_agent.type='commercial', registered_agent.cra_public_number is non-empty. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- filing.signer.printed_name_and_capacity is non-empty (form footnote ** requires signature by a duly authorized officer per 13-B MRSA §104.1.B). (depends on `filing.signer.printed_name_and_capacity`)
- If restatement.adoption_method ∈ {members_majority_at_meeting, members_supermajority_at_meeting, members_written_consent}, the MUST-BE-COMPLETED-FOR-VOTE-OF-MEMBERS clerk-attestation block must be completed (wet-ink only — no widget — but synth/rubric should track the constraint). (depends on `restatement.adoption_method`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty (per the cover letter's own rubric: 'failure to provide a contact name and telephone number or email address will result in the return of the erroneous filing(s)'). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "restatement": {
    "text_exhibit_letter": "Sample Value",
    "adoption_date": "2026-01-15",
    "adoption_method": "members_majority_at_meeting"
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
