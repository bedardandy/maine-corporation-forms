# Case-data model

Fill data is one nested object keyed by **dotted canonical keys**, reused across
every form so a downstream app builds an entity profile once and fills many
forms from it. Each form's `mapping.json` targets a subset of these keys; its
`schema.json` is the per-form view of the model.

This document describes the shared top-level groups, synthesized from the
field-mapping analysis across all 156 forms.

## Top-level groups

### `entity.*` — the business entity itself
The subject of the filing.

- `entity.name` — legal name
- `entity.home_jurisdiction`, `entity.home_jurisdiction_name` — for foreign entities
- `entity.formation_date_in_home_jurisdiction`, `entity.maine_authorization_date`
- `entity.maine_fictitious_name` — assumed/fictitious name used in Maine
- `entity.authorized_shares_total`, `entity.share_class_name`, `entity.share_structure`
  (enum: `single_class` | `multi_class`) — corporate share structure
- `entity.has_board_of_directors`, `entity.directors_count_limited`,
  `entity.directors_min_count`, `entity.directors_max_count`
- elect-in booleans: `entity.is_professional_corporation`,
  `entity.is_close_corporation`, `entity.is_benefit_corporation`,
  `entity.is_series_llc`, `entity.is_low_profit_llc`,
  `entity.director_liability_limited`, `entity.mandatory_indemnification`,
  `entity.preemptive_rights_elected`, `entity.additional_provisions_present`
- `entity.principal_office.physical_address`, `entity.principal_office.mailing_address`
- `entity.annual_report_reminder_email`

### `clerk.*` / `registered_agent.*` — the resident agent
Corporations and nonprofits use a **clerk**; LLCs/LPs/LLPs use a **registered
agent**. Same shape:

- `clerk.name` / `registered_agent.name`
- `clerk.type` / `registered_agent.type` — enum: `commercial` | `noncommercial`
- `clerk.cra_public_number` / `registered_agent.cra_public_number` —
  the state-assigned CRA public number; **required only when type = commercial**
- `clerk.physical_address` (not a P.O. Box), `clerk.mailing_address`

### `filing.*` — the submission envelope
The cover-letter / processing fields shared across almost every form.

- `filing.date_signed`, `filing.effective_date`
- `filing.entities[]` — list of entities in a multi-form bundle
  (`filing.entities[0].name`, `filing.entities[1].name`, ...)
- `filing.expedited_service` — enum: `hold_for_pickup` (no fee) |
  `24h_next_business_day` ($50/entity) | `immediate_same_day` ($100/entity)
- `filing.total_fees_dollars`
- `filing.contact.{name,phone,email}` — who to contact about this filing
- `filing.attested_copy_recipient.{name,firm}` and
  `filing.attested_copy_recipient.mailing_address.{street,city_state_zip}`
- `filing.signer.printed_name_and_capacity`,
  `filing.signer_entity.{name,signer_printed_name_and_capacity}`
- `filing.application_type` — enum: `new` | `renewal`

### Roster groups — the people/entities on the filing
Repeating roles, numbered when a form has multiple slots:

- `incorporator_1.printed_name`, `incorporator_1.address`, ...
- `officer.*`, `director.*`, `member.*`, `general_partner_1.*`, `partner.*`
- entity signers: `general_partner_entity_1.name`, `filing.signer_entity.name`
- `mark.applicant.entity_type`, `mark.charter_number`, `mark.type_and_class_number`
  (trademark/service-mark forms)

### Action-specific groups
Forms for a particular transaction carry a dedicated group:

- `merger.*`, `conversion.*`, `amendment.*`, `dissolution.*`,
  `clerk_change.*`, `restatement.*`, `revocation.*`, `domestication.*`

## Conventions

- **Booleans** for elect-ins and presence flags: keys starting `is_`/`has_` or
  ending `_elected` / `_limited` / `_present` / `_required`.
- **Integers** for counts and share quantities (`*_count`, `*_shares`,
  `authorized_shares_total`). The state-assigned CRA *public number* is a string
  (it is an identifier, not a quantity).
- **Enums** for mutually-exclusive options (`clerk.type`,
  `entity.share_structure`, `filing.expedited_service`, `filing.application_type`).
  The enum values are listed in each form's `schema.json`.
- **Addresses** are sometimes a single line (`clerk.physical_address`) and
  sometimes split (`...mailing_address.street` + `...mailing_address.city_state_zip`)
  depending on how the source form lays them out. Follow what the form's
  `schema.json` declares — the model mirrors the PDF, it does not normalize it.
- **Lists** use `[N]` indexing (`filing.entities[0].name`); the engine's
  resolver supports list indexing.
