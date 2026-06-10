# SKILL: Filling LLP_MLLP-11R

**Form:** Certificate of Renunciation (Domestic Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Renounce LLP status of a Maine domestic registered limited liability partnership under 31 MRSA §825 without affecting the partnership's underlying existence. Captures the date the original LLP certificate was filed (FIRST), the reason for renunciation (SECOND, multi-line), an optional future effective date or time (THIRD), and an optional exhibit reference for additional information (FOURTH). Filing fee $75. The certificate must be signed per §825's three-tier authority rule (see filer_role).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.llp_certificate_filing_date` | text | high | FIRST: The date of filing of its certificate of limited liability partnership was |
| `entity.name` | text | high | (Name of Limited Liability Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 31 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.llp_certificate_filing_date is non-empty and on or before filing.date_signed. (depends on `entity.llp_certificate_filing_date`, `filing.date_signed`)
- At least one of renunciation.reason.line1–line3 is non-empty. (depends on `renunciation.reason.line1`, `renunciation.reason.line2`, `renunciation.reason.line3`)
- If renunciation.future_effective_date is set, it is on or after filing.date_signed (must be a date or time certain in the future). (depends on `renunciation.future_effective_date`, `filing.date_signed`)
- At least one of filing.signer.printed_name_and_capacity, filing.signer_2.printed_name_and_capacity, filing.signer_3.printed_name_and_capacity, filing.entity_signer_1.signer_printed_name_and_capacity, filing.entity_signer_2.signer_printed_name_and_capacity, or filing.entity_signer_3.signer_printed_name_and_capacity is non-empty (per §825 three-tier authority rule). (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_2.printed_name_and_capacity`, `filing.signer_3.printed_name_and_capacity`, `filing.entity_signer_1.signer_printed_name_and_capacity`, `filing.entity_signer_2.signer_printed_name_and_capacity`, `filing.entity_signer_3.signer_printed_name_and_capacity`)
- If filing.entity_signer_N.name is set for any N, the corresponding filing.entity_signer_N.signer_printed_name_and_capacity must also be set. (depends on `filing.entity_signer_1.name`, `filing.entity_signer_1.signer_printed_name_and_capacity`, `filing.entity_signer_2.name`, `filing.entity_signer_2.signer_printed_name_and_capacity`, `filing.entity_signer_3.name`, `filing.entity_signer_3.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "llp_certificate_filing_date": "2026-01-15"
  },
  "renunciation": {
    "reason": {
      "line1": "Sample Value",
      "line2": "Sample Value",
      "line3": "Sample Value"
    },
    "future_effective_date": "2026-01-15",
    "additional_info_exhibit_letter": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
