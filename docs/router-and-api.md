# Router, HTTP API & agent integration

Three additive layers let an agent or service go from a plain-language situation
to a filled PDF. All are optional; the per-form contract and `engine/` remain the
substrate.

## 1. Form router (`tools/route_form.py`)

Ranks candidate `form_id`s for a free-text situation over a compact **router
catalog** (`catalog/router_catalog.json` — form titles + a few factual hints
derived from each form's entity type, category, and code). At ~156 forms the
catalog is ~3k tokens and fits one prompt, so no embeddings are needed.

```bash
python3 tools/route_form.py "form a new business corporation in Maine"
python3 tools/route_form.py "change our LLC registered agent" --json
```

It makes one LLM call (OpenAI-compatible, pluggable via `ROUTER_BASE_URL` /
`ROUTER_MODEL` / `ROUTER_API_KEY` / `ROUTER_TOP_K`) and **falls back to a lexical
scorer** when no endpoint is reachable, so it always returns candidates offline.
Rebuild the catalog after adding forms:

```bash
python3 tools/build_router_catalog.py
```

## 2. HTTP API (`tools/api_server.py`)

Pure standard-library (`http.server`) — no extra dependencies.

```bash
python3 tools/api_server.py --port 8080
```

| Method | Path | Body | Returns |
|--------|------|------|---------|
| GET | `/healthz` | — | `{ok, forms}` |
| GET | `/forms` | — | the form index |
| POST | `/route` | `{situation, top_k?}` | `{mode, results}` |
| POST | `/plan` | `{form, case}` | coverage plan (see `engine.plan`) |
| POST | `/fill` | `{form, case}` | filled PDF bytes (`application/pdf`) |

`/plan` and `/fill` are deterministic functions of the posted case object.

## 3. Agent (MCP) server & Codex plugin

`tools/agent_server.py` is an MCP server (stdio, FastMCP) exposing
`find_forms` / `get_form` / `plan_fill` / `fill_form`, plus this repo's extra
tools `preflight` and `fill_form_draft` (the preflight-bypass escape). It is
built on the shared `maine-forms-engine` MCP scaffold: standardized parameter
names (`query`, `case`, `out_dir`) and one error shape (failures are always
`{"ok": false, "error": ..., "error_type": ...}`).

```bash
claude mcp add maine-corporation-forms -- python3 tools/agent_server.py
```

`.mcp.json` wires the same server for any MCP client. The `.codex-plugin/`
bundle (`plugin.json` + `.mcp.json` + `skills/corp-route-and-fill/SKILL.md`) packages
the server with a directive route→plan→fill workflow skill; install via the
marketplace at `.agents/plugins/marketplace.json`. Requires `mcp`
(`pip install mcp`); the import is lazy so the module is inspectable without it.

## Not legal advice

Every path produces a draft for review, not a filed document.
