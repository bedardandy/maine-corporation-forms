# SKILL: Filling CORP_MBCA-11I

**Form:** Articles of Dissolution (by Incorporators or Initial Directors)  
**Entity type:** Business Corporation  
**When to use:** Dissolve a Maine domestic business corporation under 13-C MRSA §1401 by a majority of incorporators or initial directors — the early-dissolution path available when the corporation has not yet issued shares OR has not commenced business. Distinct from MBCA-11 (Articles of Dissolution under §1404, used after operations have begun). Captures entity name, the original incorporation-filing date, the dissolution-authorization date, optional future effective date, the FOURTH-recital basis (no shares issued OR not commenced business), and up to two signer slots.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `dissolution.authorization_date` | text | high | SECOND: The date that the dissolution was authorized is |
| `dissolution.early_dissolution_basis` | text | high | FOURTH: [ ] None of the corporation's shares have been issued. (fills multiple widgets) |
| `dissolution.effective_date` | text | high | THIRD: The effective date of the articles of dissolution (if other than the date of filing of the articles of dissolution) is |
| `entity.name` | text | high | (Name of Corporation) |
| `entity.original_articles_filing_date` | text | high | FIRST: The date of incorporation is |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.original_articles_filing_date is non-empty and is on or before filing.date_signed. (depends on `entity.original_articles_filing_date`, `filing.date_signed`)
- dissolution.authorization_date is non-empty and is on or after entity.original_articles_filing_date and on or before filing.date_signed. (depends on `dissolution.authorization_date`, `entity.original_articles_filing_date`, `filing.date_signed`)
- If dissolution.effective_date is set, it is on or after dissolution.authorization_date. (depends on `dissolution.effective_date`, `dissolution.authorization_date`)
- Exactly one of FOURTH-recital checkboxes is selected, populating dissolution.early_dissolution_basis with 'no_shares_issued' or 'not_commenced_business' (form text 'X one box only'). (depends on `dissolution.early_dissolution_basis`)
- At least filing.signer_1.printed_name_and_capacity is non-empty (form footer requires majority of incorporators/initial directors to sign). (depends on `filing.signer_1.printed_name_and_capacity`)
- Each populated signer slot's printed_name_and_capacity includes a capacity ('Incorporator' or 'Initial Director' per 13-C MRSA §1401). (depends on `filing.signer_1.printed_name_and_capacity`, `filing.signer_2.printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "original_articles_filing_date": "2026-01-15"
  },
  "dissolution": {
    "authorization_date": "2026-01-15",
    "effective_date": "2026-01-15",
    "early_dissolution_basis": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer_1": {
      "printed_name_and_capacity": "Sample Value"
    },
    "signer_2": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
