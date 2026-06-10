# Maine Corporation Forms — Open Automation Library

[![tests](https://github.com/bedardandy/maine-corporation-forms/actions/workflows/ci.yml/badge.svg)](https://github.com/bedardandy/maine-corporation-forms/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

A community-maintained, **form-by-form** library of **156 Maine Secretary of
State business-entity filing forms**, structured for programmatic filling. Every
form is a self-contained folder — machine-readable metadata, a JSON Schema for
the fill data, an AcroForm field mapping, an agent fill-guide ("skill"), and
validation rules — so any automation layer can fill a form without re-deriving
its field structure. The blank PDFs are **fetched on demand from the official
portal and never redistributed** (see [Getting the blank PDFs](#getting-the-blank-pdfs)).

It is built to be **driven by an LLM harness** — Claude Code, codex, or any MCP
client (see [Point any LLM harness at it](#point-any-llm-harness-at-it)) — and
works equally well from a plain CLI, a [docassemble](https://docassemble.org)
interview, a LangGraph node, or a custom pipeline. The fill path is
deterministic: no network and no model at runtime.

This is the corporate-filings sibling of
[**`maine-court-forms`**](https://github.com/bedardandy/maine-court-forms) and
[**`maine-probate-forms`**](https://github.com/bedardandy/maine-probate-forms):
the same per-form contract, a different subject (entity formation, amendment,
merger, dissolution, agent changes, marks).

> ⚠️ **Not legal advice — for professional use only.** This is software that
> produces *draft* forms. It is meant to be used solely as one component of a
> broader workflow that is implemented, supervised, and reviewed by a licensed
> attorney — not as a do-it-yourself substitute for legal representation. Blank
> forms are public records of the Maine Secretary of State; the surrounding
> metadata, schemas, mappings, and skills are community-maintained and AI-derived
> (see [`PROVENANCE.md`](PROVENANCE.md)), and may lag form revisions. Verify
> against the official form and current Maine law before filing. See
> [**DISCLAIMER**](DISCLAIMER.md).

## Scope — 156 forms across 7 entity types

| Prefix | Entity type | Governing law | Forms |
|--------|-------------|---------------|------:|
| `CORP_` | Business Corporation | Maine Business Corporation Act (13-C M.R.S.) | 44 |
| `NP_` | Nonprofit Corporation | Maine Nonprofit Corporation Act (13-B M.R.S.) | 39 |
| `LLC_` | Limited Liability Company | 31 M.R.S. ch. 21 | 23 |
| `LP_` | Limited Partnership | 31 M.R.S. (RULPA) | 22 |
| `LLP_` | Limited Liability Partnership | 31 M.R.S. (LLP) | 18 |
| `MARK_` | Trademark / Service Mark | 10 M.R.S. ch. 301-A | 7 |
| `GP_` | General Partnership | 31 M.R.S. (UPA) | 3 |

These PDFs ship with AcroForm fields, so the work here is *mapping* them to a
shared canonical data model (and flagging where the field names mislead).

## Point any LLM harness at it

Point an agent at the repo and say *"use this project to prepare: \<your
filing\>"*. There are two on-ramps:

- **MCP server (recommended).** `tools/agent_server.py` exposes `find_forms` /
  `get_form` / `plan_fill` / `preflight` / `fill_form` (+ `fill_form_draft`, the
  preflight-bypass escape), so the agent calls tools instead of reading docs.
  It is built on the shared `maine-forms-engine` MCP scaffold (standard
  `query`/`case`/`out_dir` parameters, one error shape). It is pre-registered via **`.mcp.json`**, or add it manually:
  ```bash
  claude mcp add maine-corporation-forms -- python3 tools/agent_server.py
  ```
  A **`.codex-plugin/`** manifest and a top-level **`skills/corp-route-and-fill/`**
  skill ship for harnesses that consume those.
- **Plain CLI / HTTP.** Route (`tools/route_form.py`) → read the form's `SKILL.md` and
  per-field confidence → build a canonical case object → preflight every check
  (`engine.preflight`) → fetch the blank (`tools/fetch_pdfs.py`) → fill
  (`engine.fill`). The protocol is in **[`AGENTS.md`](AGENTS.md)**. A
  dependency-free HTTP API (`tools/api_server.py`, `make serve`) exposes the same
  `/route` `/plan` `/fill` steps and serves the browser review UI (`web/`) at its
  root.

Every fill is a **draft to be verified** before filing, and each field carries a
**confidence** the agent should surface along with any missing facts.

## Layout

```
forms/<FORM_ID>/        one self-contained folder per form
  form.yaml             metadata: code, title, entity type, governing law, counts
  mapping.json          canonical fact-key -> AcroForm widget(s) + confidence
  schema.json           JSON Schema (draft 2020-12) for the fill data
  fields.csv            flat widget inventory (widget, page, label, key, ...)
  rubric.yaml           conditional validation checks (required-when rules)
  README.md             human doc: purpose, governing law, known ambiguities
  SKILL.md              agent fill-guide: when to use + key fields + example
catalog/
  forms_index.json      master form list (id, code, title, entity, counts)
  by_entity.json        forms grouped by entity type
  pdf_manifest.json     per-form source URL + size + SHA-256 for fetching blanks
  caselaw.json          experimental case-law background (propose-and-flag)
engine/                 deterministic fill engine (stdlib + pypdf)
  fill.py  plan.py  route.py  schema.py  canonical.py  printcopy.py
  preflight.py         one merged issue list: schema + rubric + signer + plan
  rubric.py            executes the machine-checkable rubric.yaml checks
  verify.py            pin each blank to its manifest SHA-256 (fill-time guard)
docs/                   architecture, data model, field schema, integrations,
                        router/API, templating, print-and-sign, STATUS
tools/
  fetch_pdfs.py         download blank PDFs from the official portal (verified)
  check_upstream.py     re-probe official URLs; flag forms Maine has revised
  validate_form.py      validate one form folder — the modular-improvement loop
  agent_server.py       MCP server   api_server.py   stdlib HTTP API
  export/               templating / e-sign / doc-assembly export layer
  accessibility/        PDF /TU + title + lang remediation
examples/               worked, synthetic fills (CORP_MBCA-6, LLC_MLLC-6, ...)
web/                    browser review UI (served by api_server at its root)
.mcp.json  .codex-plugin/  skills/   harness registration
NOTICE                  Maine Secretary of State attribution for the blank forms
Makefile                dev entry points: test / validate / route / plan / fill / fetch
```

## Getting the blank PDFs

The official blanks are **not redistributed** here (they are State of Maine
public records — see [`NOTICE`](NOTICE)). Fetch them on demand; each download is
verified byte-for-byte against `catalog/pdf_manifest.json`:

```bash
python3 tools/fetch_pdfs.py                    # all forms
python3 tools/fetch_pdfs.py --forms CORP_MBCA-6 # a subset
```

You only need a blank to *fill* a form. The schema, mapping, and planning work
without it.

## Staying current — detecting a revised form

Every mapping was enriched against one specific revision of the blank, pinned by
SHA-256 in `catalog/pdf_manifest.json`. Maine sometimes re-uploads a revised form
at the same URL; when that happens the widget layout can shift and a fill built
on the old mapping lands values in the wrong place. Two guards catch this:

```bash
python3 tools/check_upstream.py            # re-probe official URLs; flag CHANGED / GONE
```

`check_upstream` re-downloads each blank, hashes it, and reports any form whose
bytes no longer match the manifest. It is read-only (nothing is written to
`forms/`) and exits non-zero on any change, so it works as a scheduled
early-warning — run it from cron or CI on a weekly cadence. When it flags a form,
re-run enrichment for that form, then `--update-manifest` to adopt the new hash.

At **fill time**, `engine.fill` checks the on-disk blank against the manifest
before filling. A mismatch warns by default (the fill still runs); set
`MCORP_VERIFY_BLANK=strict` to refuse, or `=off` to skip (`MCF_VERIFY_BLANK` works as a legacy fallback). So a blank that was
silently swapped on disk cannot be filled without notice.

## Quickstart — fill a form

```bash
pip install -r requirements.txt                # pypdf, PyYAML
python3 tools/fetch_pdfs.py --forms CORP_MBCA-6 # download the blank, SHA-verified
python3 -m engine.preflight CORP_MBCA-6 examples/corp_mbca-6.case.json  # all checks, no PDF
python3 -m engine.fill CORP_MBCA-6 examples/corp_mbca-6.case.json out.pdf
```

`engine.preflight` is the one-stop validation: it merges JSON-Schema checks,
the executable `rubric.yaml` checks (`engine.rubric` — name suffixes, P.O. Box
bans, conditional requirements, date sanity, fee totals; prose-only checks
surface as `severity=manual` instead of being dropped), signer rules, and the
`engine.plan` coverage buckets into a single machine-readable issue list.
`engine.fill` runs it automatically and **refuses on error-severity issues**
(`--no-preflight` writes a partial draft anyway), then resolves the mapping
against the blank and writes the filled AcroForm. `engine.plan` remains
available on its own for the resolved/unresolved/skipped coverage view.

Checkbox-paradox ("yellow light") note: the sibling repos (court / tax) ship
this class as a warnings-only `forms/<ID>/constraints.json` evaluated by the
shared `maine_forms_engine.constraints` layer. In this repo the same class
already lives in `rubric.yaml` — "X and Y cannot both be true", "exactly one
... is selected", and mutually-exclusive signer blocks compile to executable
checks in `engine.rubric` and surface through `engine.preflight` with the
rubric's own severities — so no `constraints.json` bridge is added here.

Computed-fields ("printed arithmetic") note, same shape: the sibling repos
ship a warnings-only `forms/<ID>/computations.json` (line math printed
verbatim on the form, evaluated by `maine_forms_engine.computations` — an
omitted total is computed and filled, a supplied contradiction warns). This
repo's only filer-facing arithmetic is the cover-sheet **"Total fee(s)
enclosed: $"**, which is not field arithmetic — it is a printed base fee
plus the expedite-service checkboxes ($50 / $100 printed on the cover
sheet), and that exact class already lives in `engine/rubric.py`'s fee
checks (`a_fee`: base + expedite premium, fed by `catalog/fees.json`,
surfaced through `engine.preflight`). The rubric checks a supplied total and
warns on a mismatch; it deliberately does not invent one when the case is
silent — so no `computations.json` bridge is added here either.

## Trust & provenance

The blank PDFs are State of Maine public records. The field mappings were
produced by multimodal LLM analysis of each form and cross-checked against the
real AcroForm widget names. Every field records a **confidence**:

- **3,949 high** / **106 medium** / **4 low** across 4,059 mapped fields.
- **10 forms are hand-maintained** (listed in `tools/HAND_MAINTAINED.txt`);
  `CORP_MBCA-6` (Articles of Incorporation) is the reference, with a verified
  mapping and a worked example.
- The rest are AI-mapped — a strong starting point that needs review before
  production use.

See [`PROVENANCE.md`](PROVENANCE.md) for the full picture, including the
`fields.csv` inventory lag on forms the state has revised, and the
**experimental** statute / case-law sidecars (AI-proposed, `verified=false`,
not citations).

## Improving a form

The library is modular by design: the smallest useful change is one form folder.
Edit `forms/<ID>/mapping.json`, then validate that one form — offline, no PDF:

```bash
python3 tools/validate_form.py CORP_MBCA-6     # one form, verbose
make validate FORM=CORP_MBCA-6                  # same, via make
make coverage                                   # every form + the review worklist
```

`validate_form.py` cross-checks each mapping against the form's widget inventory
and schema, reports the confidence mix, and flags review items (a widget the
captured inventory does not list, a key not yet in the schema, low-confidence
fields). It exits non-zero only on structural breakage, so it doubles as the CI
gate. The review items it prints **are** the contribution worklist. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Status

Field schemas, mappings, skills, and rubrics are generated for all **156 forms**
(155 fillable; `MARK_mark5` is a flat reference guide with no AcroForm). The
deterministic test suite (`make test`) and per-form validator report **zero
structural errors**. Quality beyond structure is graded by per-field confidence
above; the export, print-and-sign, accessibility, and statute/case-law layers
are present but **experimental**. Contributions that verify a mapping against a
real filled output are the most valuable — see [Improving a form](#improving-a-form).
