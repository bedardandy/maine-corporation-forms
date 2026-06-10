# Maine Corporation Forms — agent guide (CLAUDE.md; same as AGENTS.md)

This repo is a form-by-form automation library for Maine Secretary of State
business-entity filing forms. You can drive it to **fill a filing form from a
structured case-data object**.

When the user says *"use this project to file/prepare \<entity action\>"*,
follow this protocol:

1. **Route:** `python3 tools/route_form.py "<the situation>"` ranks candidate
   forms over `catalog/router_catalog.json` (one LLM call when an endpoint is
   configured, with a built-in lexical fallback so it always works offline).
   Or read `catalog/by_entity.json` to scope by entity type
   (`CORP_`/`NP_`/`LLC_`/`LP_`/`LLP_`/`GP_`/`MARK_`). Many filings are
   **multi-form bundles** (e.g. Restated Articles MUST be accompanied by
   MBCA-6-1; foreign qualifications may need FICT-4): check
   `catalog/workflows.json` for the form's workflow membership and its
   required/optional companion forms. Steps marked `"inferred": true` are
   editorial lifecycle groupings; every other step quotes language printed
   on the form itself.
2. **Understand:** read `forms/<ID>/SKILL.md` (when to use + key fields +
   example) and `forms/<ID>/form.yaml` (entity type, statute, counts). Check the
   per-field `confidence` in `mapping.json` — low-confidence fields are
   unverified. For the filing fee, read `catalog/fees.json`: an `amount` is
   present only when it is literally printed on the blank form
   (`tools/extract_fees.py` regenerates it from the SHA-verified blanks);
   `amount: null` means the fee is conditional/tiered or not printed — quote
   `printed_lines` if any and point the user at the SoS fee schedule. Never
   guess a fee.
3. **Build the case data:** assemble the nested case-data object (spec in
   `docs/data-model.md`) — top-level `entity.*`, `clerk.*` /
   `registered_agent.*`, `filing.*`, and roster groups (`incorporator_1.*`,
   `officer.*`, `member.*`, `general_partner_1.*`, ...). Don't invent values;
   omit unknowns.
4. **Preflight (recommended):** `python3 -m engine.preflight <ID> case.json`
   runs *every* check at once — JSON-Schema validation, the executable
   `rubric.yaml` checks (`engine.rubric`: name suffixes, P.O. Box bans,
   conditional requirements, date sanity, fee totals, ...), signer rules, and
   the coverage plan — and returns one machine-readable issue list
   (`{ok, issues, summary, coverage}`). `severity=error` blocks `fill` by
   default; `severity=manual` entries are rubric checks that need human
   judgment — review them, don't ignore them. (`--json` for the full list.)
5. **Plan (optional, finer-grained):** `python3 -m engine.plan <ID> case.json`
   reports coverage *without* writing a PDF — which canonical keys are
   **resolved**, which are **unresolved** (missing facts), and which are
   **skipped** because a `when` condition gates them off (e.g. a
   commercial-agent CRA number when the agent is noncommercial). Preflight
   already includes this.
6. **Fill:** `python3 -m engine.fill <ID> case.json out.pdf`. Preflight runs
   automatically and the fill **refuses on error-severity issues**; pass
   `--no-preflight` (API: `preflight="off"`) to write a partial draft anyway.
7. **Verify & report:** open `out.pdf`, read back field values, and surface the
   trust level (per-field confidence), any unresolved/missing facts and
   manual-review rubric checks, and that it must be verified before filing.

## Shared engine

The drift tools (`tools/{check_upstream,fetch_pdfs}.py`) are thin shims over
the [`maine-forms-engine`](https://github.com/bedardandy/maine-forms-engine)
package (in `requirements.txt`; **required**), configured with this repo's
policy (fetch-flag probe set, transient-vs-GONE download classification), and
`tools/agent_server.py` builds on its MCP scaffold. `catalog/pdf_manifest.json`
uses the shared `{"forms": {...}}` dialect (JSON Schema ships with the
package; `tools/convert_pdf_manifest.py` performed the one-time conversion).
The pypdf fill engine (`engine/`) and the inverted mapping direction stay
local to this repo.

## Rules
- **Not legal advice.** Filled output is a draft; it must be verified against the
  official form before filing. Always say so.
- **Respect confidence.** For low/medium-confidence mappings, tell the user the
  mapping is unverified and to check field placement.
- **Reuse canonical keys.** The naming conventions are in `docs/field-schema.md`
  and the model in `docs/data-model.md`; don't invent ad-hoc keys.
- **Conditional logic.** `rubric.yaml` encodes required-when rules (e.g. CRA
  number required when the clerk is commercial). `engine.preflight` /
  `engine.rubric` execute the machine-checkable ones; checks it reports as
  `severity=manual` still need your judgment — honor them.
- **Yellow light: paradoxical selections.** Warnings list selections the
  printed form cannot carry at once (mutually-exclusive booleans, exactly-one
  enums, exclusive signer blocks). In this repo they come from `rubric.yaml`
  via `engine.rubric`/`engine.preflight` — the equivalent of the sibling
  repos' `constraints.json` layer — and warning-severity findings never block
  a fill (only error-severity preflight issues do).
- **Computed fields live in the rubric here too.** The sibling repos'
  `computations.json` layer (arithmetic printed verbatim on the form;
  engine computes an omitted total, warns on a supplied contradiction) has
  no per-form files in this repo: the cover-sheet "Total fee(s) enclosed"
  is a printed base fee plus expedite checkboxes, not field arithmetic, and
  `engine/rubric.py`'s fee checks (base + expedite premium via
  `catalog/fees.json`) already cover it at preflight. The rubric only
  checks a supplied total — it never fills one in.
- Keep filled PDFs and run artifacts out of git (see `.gitignore`).
- Licensed Apache-2.0 (`LICENSE`).
