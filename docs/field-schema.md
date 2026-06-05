# Canonical-key naming conventions

Canonical keys are dotted paths into the case-data object (see `data-model.md`).
They are deliberately stable and reused across forms so one entity profile fills
many filings.

## Category taxonomy

Every key belongs to one category, recorded as the `category` of its schema-gap
in the source analysis:

| Category | Top-level group(s) | Examples |
|----------|--------------------|----------|
| `entity` | `entity.*` | `entity.name`, `entity.authorized_shares_total`, `entity.is_close_corporation` |
| `agent` | `clerk.*`, `registered_agent.*` | `clerk.name`, `registered_agent.cra_public_number` |
| `officer` | roster groups | `incorporator_1.printed_name`, `officer.*`, `general_partner_1.*` |
| `filing` | `filing.*` | `filing.contact.email`, `filing.expedited_service`, `filing.entities[0].name` |
| `address` | nested `*.address` / `*.mailing_address` | `filing.attested_copy_recipient.mailing_address.city_state_zip` |
| action | `merger.*`, `conversion.*`, `amendment.*`, ... | `merger.fourth_election`, `amendment.approval_method` |
| `mark` | `mark.*` | `mark.applicant.entity_type`, `mark.charter_number` |

## Naming rules

- **Lowercase, dot-separated, snake_case segments**: `filing.contact.phone`.
- **Booleans** read as predicates: prefix `is_` / `has_`, or suffix `_elected`
  / `_limited` / `_present` / `_required`. The generator types these as
  `boolean` in `schema.json`.
- **Counts and quantities** end in `_count` or `_shares` (or contain a numeric
  `number`, excluding phone and the CRA *public number*) and type as `integer`.
- **Enums** are `string` with an explicit `enum` list, declared in the form's
  `schema.json`. Values are lower_snake (`single_class`, `immediate_same_day`).
- **Repeating roles** carry a numeric suffix on the group:
  `incorporator_1.*`, `general_partner_2.*`. List-valued collections use
  `[N]` indexing: `filing.entities[0].name`.
- **Addresses** are modeled as the form presents them: a single concatenated
  line (`clerk.physical_address`) or split components
  (`...mailing_address.street`, `...mailing_address.city_state_zip`). Don't
  invent a normalized address shape the form doesn't have.

## Where the types come from

The generator infers each leaf type from the key name and the field
description:

1. Description contains `Enum:` → `string` + `enum` (parsed from the description).
2. Boolean-shaped key name or "Boolean" in the description → `boolean`.
3. Count/shares/number key name → `integer`.
4. Otherwise → `string`.

This is a heuristic. When reviewing a form, confirm the type against the
rendered PDF and the rubric, and fix `schema.json` if needed.
