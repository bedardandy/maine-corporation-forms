# SKILL: Filling NP_MNPCA-10C

**Form:** Articles of Merger (Merger of Domestic and Foreign Nonprofit Corporations)  
**Entity type:** Nonprofit Corporation  
**When to use:** File Articles of Merger between a Maine domestic nonprofit corporation and one or more foreign corporations under 13-B MRSA §906. Records the two participating corporations and their home jurisdictions, public-vs-mutual benefit classification (only when the surviving corp is Maine), the foreign jurisdictions whose laws permit the merger, the surviving corporation's identity / governing law / service-of-process address (when foreign), the plan-of-merger exhibit, the domestic corporation's adoption method (4 mutually-exclusive options), registered-office addresses for both corps, optional future effective date, and dual signature blocks with member-vote certifications.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

_Showing 12 of 38 canonical keys — the full set is in mapping.json._

## Conditional logic

- merger.merging_corp.name is non-empty. (depends on `merger.merging_corp.name`)
- merger.merging_corp.home_jurisdiction is non-empty. (depends on `merger.merging_corp.home_jurisdiction`)
- merger.surviving_corp.name is non-empty. (depends on `merger.surviving_corp.name`)
- merger.surviving_corp.home_jurisdiction is non-empty. (depends on `merger.surviving_corp.home_jurisdiction`)
- At least one of merger.merging_corp.home_jurisdiction or merger.surviving_corp.home_jurisdiction is not 'Maine' (the form is for domestic-FOREIGN mergers; an all-Maine merger uses NP_MNPCA-10). (depends on `merger.merging_corp.home_jurisdiction`, `merger.surviving_corp.home_jurisdiction`)
- At least one of merger.merging_corp.home_jurisdiction or merger.surviving_corp.home_jurisdiction equals 'Maine' (the form requires a Maine party — a foreign-foreign merger doesn't file with Maine SOS). (depends on `merger.merging_corp.home_jurisdiction`, `merger.surviving_corp.home_jurisdiction`)
- If merger.surviving_corp.home_jurisdiction = 'Maine', exactly one of merger.surviving_corp.benefit_type ∈ {'public_benefit', 'mutual_benefit'} is selected (FIRST recital). Not required when surviving corp is foreign. (depends on `merger.surviving_corp.home_jurisdiction`, `merger.surviving_corp.benefit_type`)
- merger.foreign_corp_states is non-empty (SECOND requires identifying the foreign jurisdiction(s) whose laws permit the merger). (depends on `merger.foreign_corp_states`)
- If merger.surviving_corp.home_jurisdiction != 'Maine', merger.surviving_corp.service_of_process_address must be non-empty (the foreign survivor must designate an address for SOS-forwarded process). (depends on `merger.surviving_corp.home_jurisdiction`, `merger.surviving_corp.service_of_process_address`)
- Field 8 (THIRD restated surviving corp name) equals merger.surviving_corp.name; field 9 (THIRD governing law) equals merger.surviving_corp.home_jurisdiction. (depends on `merger.surviving_corp.name`, `merger.surviving_corp.home_jurisdiction`)
- merger.plan_exhibit_letter is non-empty. (depends on `merger.plan_exhibit_letter`)
- Exactly one merger.domestic_corp.vote_method option is selected. (depends on `merger.domestic_corp.vote_method`)
- merger.domestic_corp.vote_method_date is non-empty (paired with the selected vote_method). (depends on `merger.domestic_corp.vote_method`, `merger.domestic_corp.vote_method_date`)
- merger.domestic_corp.name equals whichever of merger.surviving_corp.name or merger.merging_corp.name has home_jurisdiction='Maine'. (depends on `merger.domestic_corp.name`, `merger.surviving_corp.name`, `merger.merging_corp.name`, `merger.surviving_corp.home_jurisdiction`, `merger.merging_corp.home_jurisdiction`)
- Both merger.surviving_corp.registered_office_address_line2 and merger.merging_corp.registered_office_address_line2 are non-empty (per page-1 footnote, use principal/registered office wherever located if no Maine office). (depends on `merger.surviving_corp.registered_office_address_line2`, `merger.merging_corp.registered_office_address_line2`)
- If merger.future_effective_date is set, it must be on or after filing.date_signed AND no later than filing.date_signed + 60 days (per the SEVENTH cap noted on form). (depends on `merger.future_effective_date`)
- Each corp's signature block has signer_1.printed_name_and_capacity and date_signed populated; signer_2 may be empty unless the entity type requires two signers. (depends on `merger.surviving_corp.signature_block.signer_1.printed_name_and_capacity`, `merger.surviving_corp.signature_block.date_signed`, `merger.merging_corp.signature_block.signer_1.printed_name_and_capacity`, `merger.merging_corp.signature_block.date_signed`)

## Example case data

```json
{
  "merger": {
    "merging_corp": {
      "name": "Sample Value",
      "home_jurisdiction": "Sample Value"
    },
    "surviving_corp": {
      "name": "Sample Value",
      "home_jurisdiction": "Sample Value",
      "benefit_type": "public_benefit",
      "service_of_process_address": "Sample Value"
    },
    "foreign_corp_states": "Sample Value",
    "plan_exhibit_letter": "Sample Value"
  }
}
```
