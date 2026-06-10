# SKILL: Filling NP_FICT-4

**Form:** Statement of Intention to Do Business Under a Fictitious Name (Foreign Entities Only)  
**Entity type:** Nonprofit Corporation  
**When to use:** Foreign-entity-only filing declaring intent to transact business in Maine under a fictitious name when the entity's real name is unavailable in this State per 31 MRSA §1508 / 13-C MRSA §1505. The PDF is shared across entity types — the page-0 footnotes enumerate authorizing statutes for foreign business corporations (§1505), foreign LLCs (§1626), foreign LPs (§1308), foreign LLPs (§869), and foreign nonprofits (§1304). The NP_FICT-4 alias names the nonprofit-only invocation of the shared form (filing fee $25); CORP_FICT-4 names the for-profit invocation (filing fee $40). Identical widget composition to CORP_FICT-4 (md5-identical PDF).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | SECOND: Jurisdiction of incorporation/organization ___ and the date on which |
| `entity.home_jurisdiction_name` | text | high | (Exact Legal Name of Entity on the records of the Secretary of State) |
| `entity.maine_authorization_date` | text | high | the entity was authorized to transact business in Maine |
| `entity.maine_fictitious_name` | text | high | FIRST: The entity must transact business under the fictitious name of |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.maine_fictitious_name is non-empty. (depends on `entity.maine_fictitious_name`)
- entity.maine_fictitious_name differs from entity.home_jurisdiction_name (case-insensitive) — the whole point of a fictitious-name filing is to use a different name in Maine. (depends on `entity.maine_fictitious_name`, `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and is not 'Maine' or 'ME' (this form is foreign-only). (depends on `entity.home_jurisdiction`)
- entity.maine_authorization_date is non-empty and not in the future (entity must already be qualified in Maine to register a fictitious name). (depends on `entity.maine_authorization_date`)
- filing.date_signed is on or after entity.maine_authorization_date (you can't file a fictitious-name statement before being authorized to transact business). (depends on `filing.date_signed`, `entity.maine_authorization_date`)
- filing.signer.printed_name and filing.signer.title are both non-empty (Shape A pattern; statute restricts authorized signers per entity type). (depends on `filing.signer.printed_name`, `filing.signer.title`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name": "Sample Value",
      "title": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    }
  }
}
```
