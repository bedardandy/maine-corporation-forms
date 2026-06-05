# SKILL: Filling LLC_MLLCSOA

**Form:** Statement of Authority (for a Maine LLC)  
**Entity type:** Limited Liability Company  
**When to use:** File a Statement of Authority under 31 MRSA §1542.1 to grant or limit the authority of specific persons or existing positions to enter into transactions or otherwise bind a Maine LLC. Supports up to three inline authority blocks (each: a person or position name + four free-form authority/limitation text lines), an optional exhibit letter for additional authority blocks beyond three, and up to three authorized signers (filing.signer_N pattern) — some entity-level decisions under 31 MRSA require multiple signers.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `authority.additional_exhibit_letter` | text | high | Additional information is set forth in the attached Exhibit ____, and made a part hereof. |
| `authority_1.authority_text_line_1` | text | high | Authority granted or limitations: (line 1) |
| `authority_1.authority_text_line_2` | text | high | Authority granted or limitations: (line 2) |
| `authority_1.authority_text_line_3` | text | high | Authority granted or limitations: (line 3) |
| `authority_1.authority_text_line_4` | text | high | Authority granted or limitations: (line 4) |
| `authority_1.person_or_position` | text | high | (name of person or position) |
| `authority_2.authority_text_line_1` | text | high | Authority granted or limitations: (line 1) |
| `authority_2.authority_text_line_2` | text | high | Authority granted or limitations: (line 2) |
| `authority_2.authority_text_line_3` | text | high | Authority granted or limitations: (line 3) |
| `authority_2.authority_text_line_4` | text | high | Authority granted or limitations: (line 4) |
| `authority_2.person_or_position` | text | high | (name of person or position) |
| `authority_3.authority_text_line_1` | text | high | Authority granted or limitations: (line 1) |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- authority_1.person_or_position is non-empty (the form requires at least one person or position to have a documented grant or limitation — otherwise the filing has no purpose). (depends on `authority_1.person_or_position`)
- For each N in {1,2,3}: if authority_N.person_or_position is non-empty, authority_N.authority_text_line_1 must also be non-empty (a person/position with no recited authority/limitation is malformed). (depends on `authority_1.person_or_position`, `authority_1.authority_text_line_1`, `authority_2.person_or_position`, `authority_2.authority_text_line_1`, `authority_3.person_or_position`, `authority_3.authority_text_line_1`)
- filing.signer_1.printed_name_and_capacity is non-empty. (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.entities[0].name equals entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "authority_1": {
    "person_or_position": "Sample Value",
    "authority_text_line_1": "Sample Value",
    "authority_text_line_2": "Sample Value",
    "authority_text_line_3": "Sample Value",
    "authority_text_line_4": "Sample Value"
  },
  "authority_2": {
    "person_or_position": "Sample Value",
    "authority_text_line_1": "Sample Value"
  }
}
```
