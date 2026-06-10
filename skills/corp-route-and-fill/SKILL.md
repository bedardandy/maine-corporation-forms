---
name: corp-route-and-fill
description: Fill a Maine Secretary of State business-entity filing form from a plain-language situation. Use when the user wants to prepare/file a corporation, LLC, LP, LLP, partnership, nonprofit, or trademark filing.
---

# Route and fill a Maine SoS entity form

Use the project's `tools/` and `engine/` layer — **ignore** any heavier pipeline.
Filling is deterministic, no network and no LLM at fill time.

## Workflow

1. **Route.** `python3 tools/route_form.py "<the situation>"` (or the
   `find_forms` MCP tool) ranks candidate `form_id`s. Pick one and confirm with
   the user when ambiguous.

2. **Understand.** Read `forms/<ID>/SKILL.md` and `forms/<ID>/form.yaml`
   (entity type, statute, fee). Check per-field `confidence` in `mapping.json` —
   low/medium-confidence fields are unverified; tell the user.

3. **Plan.** `python3 -m engine.plan <ID> case.json` (or the `plan_fill` MCP
   tool) reports coverage: **resolved**, **unresolved** (missing facts;
   `required: true` are blocking per the rubric), and **skipped** (gated off by a
   `when` condition, e.g. a commercial-agent CRA number when the agent is
   noncommercial). Collect the missing required facts before filling.

4. **Fill.** `python3 -m engine.fill <ID> case.json out.pdf` (or the `fill_form`
   MCP tool). The case object is a nested dict — `entity.*`, `clerk.*` /
   `registered_agent.*`, `filing.*`, and roster groups (`incorporator_1.*`,
   `officer.*`, `general_partner_1.*`, ...). See `docs/data-model.md`. Don't
   invent values; omit unknowns.

5. **Verify & report.** Open `out.pdf`, read field values back, and surface the
   trust level, any unresolved/missing facts, and that the draft must be verified
   against the official form before filing.

## Rules

- **Not legal advice.** The output is a draft for review, not a filed document.
- **Reuse canonical keys** (`docs/field-schema.md`); don't invent ad-hoc keys.
- **Honor `rubric.yaml`** required-when rules and the planner's `skipped` set.
