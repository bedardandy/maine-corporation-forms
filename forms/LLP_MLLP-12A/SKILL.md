# SKILL: Filling LLP_MLLP-12A

**Form:** Amended Application for Authority to Do Business (Foreign LLP)  
**Entity type:** Limited Liability Partnership  
**When to use:** Amend the authority of a foreign LLP to do business in Maine under 31 MRSA §855 (sibling of MLLC-12A for foreign LLCs and CORP_MBCA-12A for foreign corporations). Updates may include the home-jurisdiction name (FIRST), the Maine fictitious name and accompanying FICT-4 (SECOND), the nature of business (THIRD), the principal-office address (FOURTH), and the contact partner's name/address (FIFTH). SIXTH allows an exhibit-attached catch-all for other amendments. Each amendment paragraph follows the standard 'If no change, so indicate.' convention — empty values mean no change to that item.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `contact_partner.address` | text | high | FIFTH: ...Address |
| `contact_partner.name` | text | high | FIFTH: The name and or the business, residence or mailing address of the contact partner has been changed to: (If no change, so indicate.) — Name |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction_name` | text | high | FIRST: The name of the limited liability partnership in its jurisdiction of organization has been changed to ___ (If no change, so indicate.) |
| `entity.home_jurisdiction_name_on_record` | text | high | (Name of Limited Liability Partnership in Jurisdiction of Organization) — top-of-form identifier |
| `entity.maine_business_purpose` | text | high | THIRD: The nature of the business or purposes to be conducted or promoted in the State of Maine is ___ (If no change, so indicate.) |
| `entity.maine_fictitious_name` | text | high | SECOND: If the real limited liability partnership name is not available, the fictitious name under which it proposes to apply for authority to do business in the State of Maine is ___ (If applicable, so indicate.) |
| `entity.principal_office.mailing_address` | text | high | (mailing address if different from above) |
| `entity.principal_office.physical_address` | text | high | FOURTH: The new address of the registered or principal office, wherever located, is: (If no change, so indicate.) (physical location - street (not P.O. Box), city, state and zip code) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |

## Conditional logic

- entity.home_jurisdiction_name_on_record is non-empty (top-of-form recital used to identify the existing SOS record). (depends on `entity.home_jurisdiction_name_on_record`)
- At least one of FIRST (entity.home_jurisdiction_name), SECOND (entity.maine_fictitious_name), THIRD (entity.maine_business_purpose), FOURTH (entity.principal_office.*), FIFTH (contact_partner.*), or SIXTH (filing.other_amendments_exhibit_letter) carries a non-empty, non-'No change' value (an amendment that changes nothing is vacuous). (depends on `entity.home_jurisdiction_name`, `entity.maine_fictitious_name`, `entity.maine_business_purpose`, `entity.principal_office.physical_address`, `entity.principal_office.mailing_address`, `contact_partner.name`, `contact_partner.address`, `filing.other_amendments_exhibit_letter`)
- If entity.maine_fictitious_name is set to a non-'No change' value (i.e., adopting or changing a fictitious name), filing.fict4_accompanies must be true. (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- If entity.principal_office.physical_address is set to a non-'No change' value, it must not start with 'P.O. Box' (per FOURTH parenthetical 'street (not P.O. Box)'). (depends on `entity.principal_office.physical_address`)
- Exactly one signer block is populated: either filing.signer.printed_name_and_capacity (individual partner) OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) (entity partner). Both blocks empty or both populated is a fill error. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- If filing.signer_entity.name is populated, filing.signer_entity.signer_printed_name_and_capacity must also be populated. (depends on `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- If contact_partner.name is set to a non-'No change' value, contact_partner.address must also be set (and vice versa). (depends on `contact_partner.name`, `contact_partner.address`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- At most one of the three expedite checkboxes is selected. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name_on_record": "Wabanaki Widgets, Inc.",
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "maine_business_purpose": "Sample Value",
    "principal_office": {
      "physical_address": "Sample Value",
      "mailing_address": "Sample Value"
    }
  },
  "filing": {
    "fict4_accompanies": "Sample Value"
  },
  "contact_partner": {
    "name": "Sample Value"
  }
}
```
