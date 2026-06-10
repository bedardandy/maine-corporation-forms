# SKILL: Filling LLP_MLLP-6

**Form:** Certificate of Limited Liability Partnership  
**Entity type:** Limited Liability Partnership  
**When to use:** Form a domestic Maine Limited Liability Partnership under 31 MRSA §822 (also referenced on the form as the LLP qualification statement). Captures: optional professional-LLP election under 13 MRSA Chapter 22-A; the LLP's name (with statutory suffix per §803-A); registered agent (commercial or noncommercial) with physical and optional mailing address; the contact partner's name and address; an optional additional-provisions exhibit; and up to 3 individual-partner signature slots plus 3 entity-partner signature slots.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `contact_partner.address` | text | high | FOURTH (split): Address (right column) |
| `contact_partner.name` | text | high | FOURTH (split): Name (left column) |
| `entity.additional_provisions_exhibit_letter` | text | high | FIFTH: Other provisions of this certificate, if any, that the partners determine to include are set forth in Exhibit ___ attached hereto and made a part hereof. |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.is_professional_llp` | checkbox | high | [ ] Mark box only if applicable. This is a professional limited liability partnership* formed pursuant to 13 MRSA Chapter 22-A |
| `entity.name` | text | high | FIRST: The name of the registered limited liability partnership is |
| `entity.professional_services_description` | text | high | (type of professional services) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |

_Showing 12 of 36 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty and contains a statutory LLP suffix ('Limited Liability Partnership', 'L.L.P.', or 'LLP') per 31 MRSA §803-A. (depends on `entity.name`)
- If entity.is_professional_llp is true, entity.professional_services_description must be non-empty. (depends on `entity.is_professional_llp`, `entity.professional_services_description`)
- Exactly one of SECOND commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- registered_agent.name is non-empty (in either Text4 commercial slot or Text5 noncommercial slot, matching the selected type). (depends on `registered_agent.name`, `registered_agent.type`)
- If registered_agent.type='commercial', registered_agent.cra_public_number must be set. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address is non-empty and is not a P.O. Box. (depends on `registered_agent.physical_address`)
- Either contact_partner.name AND contact_partner.address are populated (split widgets) OR contact_partner.name_and_address is populated (combined widget). (depends on `contact_partner.name`, `contact_partner.address`, `contact_partner.name_and_address`)
- If entity.additional_provisions_exhibit_letter is populated, it must be a single uppercase letter A-Z. (depends on `entity.additional_provisions_exhibit_letter`)
- At least one of {partner_1.printed_name, partner_2.printed_name, partner_3.printed_name, partner_entity_1.signer_printed_name_and_capacity, partner_entity_2.signer_printed_name_and_capacity, partner_entity_3.signer_printed_name_and_capacity} is non-empty (per page-1 footnote requirement: '(1) one or more partners who are authorized OR (2) any duly authorized person'). (depends on `partner_1.printed_name`, `partner_2.printed_name`, `partner_3.printed_name`, `partner_entity_1.signer_printed_name_and_capacity`, `partner_entity_2.signer_printed_name_and_capacity`, `partner_entity_3.signer_printed_name_and_capacity`)
- If partner_entity_N.name is populated, partner_entity_N.signer_printed_name_and_capacity must also be populated (and vice versa) for each N in 1..3. (depends on `partner_entity_1.name`, `partner_entity_1.signer_printed_name_and_capacity`, `partner_entity_2.name`, `partner_entity_2.signer_printed_name_and_capacity`, `partner_entity_3.name`, `partner_entity_3.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "is_professional_llp": true,
    "professional_services_description": "Sample Value",
    "name": "Wabanaki Widgets, Inc."
  },
  "registered_agent": {
    "cra_public_number": "P99999",
    "type": "Sample Value",
    "name": "Sample Value",
    "physical_address": "Sample Value",
    "mailing_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
