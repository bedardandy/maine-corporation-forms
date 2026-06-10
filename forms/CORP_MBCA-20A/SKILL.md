# SKILL: Filling CORP_MBCA-20A

**Form:** Articles of Charter Surrender (Upon Nonprofit Conversion)  
**Entity type:** Business Corporation  
**When to use:** Surrender the Maine charter of a domestic business corporation when it converts to a FOREIGN nonprofit corporation under 13-C MRSA §§934 and 935. The filing records the effective date of the foreign conversion (FIRST), recites shareholder approval (SECOND, no widget), identifies the new (non-Maine) jurisdiction of incorporation (THIRD), appoints the Secretary of State as agent for service of process re shareholder appraisal rights and provides a forwarding mailing address (FOURTH), and recites the surviving entity's obligation to pay appraisal-rights amounts under chapter 13 (FIFTH, no widget). Filing fee is $90 per the page-0 header. 2 pages, 20 widgets.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.future_effective_date` | text | high | FIRST: ... and the effective date of the conversion is (date) ___ |
| `conversion.new_jurisdiction` | text | high | THIRD: The corporation's new jurisdiction of incorporation is ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.appraisal_rights_agent_mailing_address` | text | high | FOURTH: ... shall provide a mailing address to which the Secretary of State may mail a copy of any process served on the Secretary of State (mailing address) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- conversion.future_effective_date is non-empty (FIRST is mandatory on this form, unlike MBCA-20's optional FOURTH). (depends on `conversion.future_effective_date`)
- conversion.new_jurisdiction is non-empty and is NOT 'Maine' / 'ME' (the form is specifically for outbound conversion to a foreign jurisdiction). (depends on `conversion.new_jurisdiction`)
- filing.appraisal_rights_agent_mailing_address is non-empty (FOURTH mandates it). (depends on `filing.appraisal_rights_agent_mailing_address`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D; signer must be 'an officer or other duly authorized representative' per 13-C MRSA §934.1). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "conversion": {
    "future_effective_date": "2026-01-15",
    "new_jurisdiction": "Sample Value"
  },
  "filing": {
    "appraisal_rights_agent_mailing_address": "Sample Value",
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    }
  }
}
```
