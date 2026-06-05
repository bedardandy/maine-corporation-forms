# Maine Corporation Forms — agent guide (CLAUDE.md; same as AGENTS.md)

This repo is a form-by-form automation library for Maine Secretary of State
business-entity filing forms. You can drive it to **fill a filing form from a
structured case-data object**.

When the user says *"use this project to file/prepare \<entity action\>"*,
follow this protocol:

1. **Route:** `python3 -m engine.route "<the situation>"` ranks candidate forms
   by lexical overlap over `catalog/forms_index.json` (title + code + entity
   type). Or read `catalog/by_entity.json` to scope by entity type
   (`CORP_`/`NP_`/`LLC_`/`LP_`/`LLP_`/`GP_`/`MARK_`).
2. **Understand:** read `forms/<ID>/SKILL.md` (when to use + key fields +
   example) and `forms/<ID>/form.yaml` (entity type, statute, counts). Check the
   per-field `confidence` in `mapping.json` — low-confidence fields are
   unverified.
3. **Build the case data:** assemble the nested case-data object (spec in
   `docs/data-model.md`) — top-level `entity.*`, `clerk.*` /
   `registered_agent.*`, `filing.*`, and roster groups (`incorporator_1.*`,
   `officer.*`, `member.*`, `general_partner_1.*`, ...). Don't invent values;
   omit unknowns.
4. **Validate (optional):** `engine.schema.validate(form_id, case_data)` checks
   types, enums, and required keys against `forms/<ID>/schema.json`.
5. **Plan (recommended):** `python3 -m engine.plan <ID> case.json` reports
   coverage *without* writing a PDF — which canonical keys are **resolved**,
   which are **unresolved** (missing facts; `required: true` are blocking per
   the rubric), and which are **skipped** because a `when` condition gates them
   off (e.g. a commercial-agent CRA number when the agent is noncommercial).
   Use it to collect missing facts before filling.
6. **Fill:** `python3 -m engine.fill <ID> case.json out.pdf`.
7. **Verify & report:** open `out.pdf`, read back field values, and surface the
   trust level (per-field confidence), any unresolved/missing facts, and that it
   must be verified before filing.

## Rules
- **Not legal advice.** Filled output is a draft; it must be verified against the
  official form before filing. Always say so.
- **Respect confidence.** For low/medium-confidence mappings, tell the user the
  mapping is unverified and to check field placement.
- **Reuse canonical keys.** The naming conventions are in `docs/field-schema.md`
  and the model in `docs/data-model.md`; don't invent ad-hoc keys.
- **Conditional logic.** `rubric.yaml` encodes required-when rules (e.g. CRA
  number required when the clerk is commercial). Honor them.
- Keep filled PDFs and run artifacts out of git (see `.gitignore`).
- Licensed Apache-2.0 (`LICENSE`).
