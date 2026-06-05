# SKILL: Filling NP_MNPCA-19

**Form:** Articles of Domestication and Conversion (Foreign Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Domesticate and convert a foreign nonprofit corporation into a Maine nonprofit corporation. Records the foreign entity's name in its home jurisdiction, the proposed Maine name (if unavailable in foreign form), home jurisdiction, original incorporation date, attached new Articles of Incorporation exhibit (per FORM MBCA-6-1 reference in the template), and an optional future effective date. Page-0 header recites '13-C MRSA §942' but the page-0 banner is FOREIGN NONPROFIT CORPORATION — see open_questions: this is the same upstream template-text quirk seen on NP_MNPCA-19A (template appears forked from CORP_MBCA-19 without updating Title 13-C statutory references for the 13-B nonprofit equivalent).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `domestication.articles_exhibit_letter` | text | high | THIRD: All the statements required to be set forth in Articles of Incorporation (MBCA-6-1) are attached as Exhibit ___ |
| `domestication.future_effective_date` | text | high | FOURTH: The effective date of the articles of domestication and conversion (if other than the date of filing of the articles of domestication and conversion) is ___ |
| `domestication.maine_name` | text | high | FIRST: If the real corporate name is not available in this state... the name it proposes to use in the State of Maine: |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | and the original date of incorporation was ___ |
| `entity.home_jurisdiction` | text | high | FIRST: The corporation was originally incorporated in ___ (state or country) |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation in Jurisdiction of Incorporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |

## Conditional logic

- entity.home_jurisdiction_name is non-empty (foreign-only form per FOREIGN NONPROFIT CORPORATION page-0 banner). (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty. (depends on `entity.home_jurisdiction`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (domestication implies a non-Maine origin). (depends on `entity.home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is non-empty and parses as a date on or before filing.date_signed. (depends on `entity.formation_date_in_home_jurisdiction`, `filing.date_signed`)
- domestication.articles_exhibit_letter is non-empty (the new-entity Articles of Incorporation exhibit must be attached). (depends on `domestication.articles_exhibit_letter`)
- If domestication.future_effective_date is set, it must be on or after filing.date_signed. (depends on `domestication.future_effective_date`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (form footer requires 'an officer or other duly authorized representative'). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive: per the cover-letter NOTE 'Failure to provide a contact name and telephone number or email address will result in the return of the erroneous filing(s)'). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "formation_date_in_home_jurisdiction": "2026-01-15"
  },
  "domestication": {
    "maine_name": "Sample Value",
    "articles_exhibit_letter": "Sample Value",
    "future_effective_date": "2026-01-15"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
