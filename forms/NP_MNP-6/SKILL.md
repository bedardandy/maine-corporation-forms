# SKILL: Filling NP_MNP-6

**Form:** Certificate of Organization (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Form a Maine domestic nonprofit corporation under 13 MRSA §903 (older 'MNP-' prefixed form, predecessor to NP_MNPCA-6 under 13-B MRSA). Captures entity name (FIRST), public-benefit vs mutual-benefit selection with a free-text purpose block (THIRD, two parallel checkboxes plus two free-text blocks), municipality + county location (FOURTH), four named officer slots — President / Vice-President / Secretary or Clerk / Treasurer (FIFTH) plus an officer count, three directors/trustees (SIXTH), an entity-level contact person with mailing + physical address (SEVENTH), the signature/dating block, and up to ~6 individual incorporator rows (each with printed name, street, city/state/zip — wet-ink signatures). Filing fee is $5 per the page-0 header. 3 pages, 51 widgets. Distinct from NP_MNPCA-6 in that this older form has no registered-agent block, no member-class election, and no 501(c) opt-ins; instead it has the named officer roster + entity-contact-person block.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `director_1.name` | text | high | SIXTH: The Directors or Trustees are: ___ (row 1) |
| `director_2.name` | text | high | SIXTH: ___ (row 2) |
| `director_3.name` | text | high | SIXTH: ___ (row 3) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.contact_person.mailing_address` | text | high | SEVENTH: ___ (mailing address) |
| `entity.contact_person.name` | text | high | SEVENTH: Contact person: ___ (name) |
| `entity.contact_person.physical_address` | text | high | SEVENTH: ___ (physical address) |
| `entity.location.county` | text | high | FOURTH: ___ (county) |
| `entity.location.municipality` | text | high | FOURTH: It is located in ___ (municipality) |
| `entity.mutual_benefit_purpose` | text | high | THIRD: ...purpose or purposes: (Mutual Benefit free-text block) |
| `entity.name` | text | high | FIRST: The name of the corporation is |
| `entity.nonprofit_type` | text | high | THIRD: [X] The corporation is organized as a public benefit corporation for the following purpose or purposes: (fills multiple widgets) |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of THIRD options (Check Box2 = public_benefit, Check Box3 = mutual_benefit) is selected. (depends on `entity.nonprofit_type`)
- If entity.nonprofit_type='public_benefit', entity.public_benefit_purpose must be non-empty. If entity.nonprofit_type='mutual_benefit', entity.mutual_benefit_purpose must be non-empty. (depends on `entity.nonprofit_type`, `entity.public_benefit_purpose`, `entity.mutual_benefit_purpose`)
- entity.location.municipality and entity.location.county are both non-empty (FOURTH recital is mandatory). (depends on `entity.location.municipality`, `entity.location.county`)
- entity.officers.count equals the number of populated entity.officers.<role>.name slots (typically 4). (depends on `entity.officers.count`, `entity.officers.president.name`, `entity.officers.vice_president.name`, `entity.officers.secretary_or_clerk.name`, `entity.officers.treasurer.name`)
- entity.officers.president.name, entity.officers.vice_president.name, entity.officers.secretary_or_clerk.name, and entity.officers.treasurer.name are all non-empty (FIFTH lists all four roles inline). (depends on `entity.officers.president.name`, `entity.officers.vice_president.name`, `entity.officers.secretary_or_clerk.name`, `entity.officers.treasurer.name`)
- director_1.name is non-empty (SIXTH provides 3 inline slots; at least one must be filled). (depends on `director_1.name`)
- entity.contact_person.name and entity.contact_person.mailing_address are non-empty (SEVENTH). (depends on `entity.contact_person.name`, `entity.contact_person.mailing_address`)
- At least 3 incorporators have printed_name populated (per page-1 footnote 'Pursuant to 13 MRSA §901, at least 3 incorporators are required'). (depends on `incorporator_1.printed_name`, `incorporator_2.printed_name`, `incorporator_3.printed_name`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "nonprofit_type": "Sample Value",
    "public_benefit_purpose": "Sample Value",
    "mutual_benefit_purpose": "Sample Value",
    "location": {
      "municipality": "Sample Value",
      "county": 100
    },
    "officers": {
      "count": 100,
      "president": {
        "name": "Wabanaki Widgets, Inc."
      }
    }
  }
}
```
