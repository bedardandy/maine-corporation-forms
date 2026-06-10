#!/usr/bin/env python3
"""MCP server exposing the Maine SoS corporation-forms library to agents.

Built on the shared ``maine-forms-engine`` MCP scaffold
(``maine_forms_engine.mcp``): this module supplies the repo backend (routing,
enriched payloads, the pypdf fill path); the scaffold supplies the
standardized tool surface and the one error shape (every failure is
``{"ok": False, "error": ..., "error_type": ...}``, never a raised
exception).

Tools (stdio, FastMCP):
  find_forms(query, top_k=5)            -> candidate forms (router), each
                                           annotated with workflow membership
  get_form(form_id)                     -> metadata + trust summary (per-field
                                           confidence), printed filing fee,
                                           workflows, SKILL.md excerpt
  plan_fill(form_id, case)              -> coverage plan (resolved/unresolved/skipped)
  preflight(form_id, case)              -> every check at once (schema + rubric +
                                           signer rules + plan)         [extra tool]
  fill_form(form_id, case, out_dir)     -> preflight-gated fill, returns
                                           {ok, path, report}
  fill_form_draft(form_id, case, out_dir) -> the old no_preflight=true escape:
                                           fill a partial draft anyway  [extra tool]

Run:      python3 tools/agent_server.py
Register: claude mcp add maine-corporation-forms -- python3 tools/agent_server.py

Requires ``mcp`` (pip install 'maine-forms-engine[mcp]'). The import is lazy
so the module documents itself even without the dependency installed.
"""
from __future__ import annotations

import functools
import json
import pathlib
import re
import sys

from maine_forms_engine.mcp import UnknownFormError
from maine_forms_engine.mcp.server import main as _scaffold_main

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

_FORMS_ROOT = str(ROOT / "forms")
_MAX_UNVERIFIED = 15  # cap field lists so get_form stays compact


@functools.lru_cache(maxsize=None)
def _catalog(name: str) -> dict:
    path = ROOT / "catalog" / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@functools.lru_cache(maxsize=None)
def _workflow_membership() -> dict:
    """form_id -> [{id, title, required}] from catalog/workflows.json."""
    member: dict = {}
    for wf in _catalog("workflows.json").get("workflows", []):
        for step in wf["steps"]:
            member.setdefault(step["form_id"], []).append({
                "id": wf["id"], "title": wf["title"],
                "required": step["required"],
            })
    return member


def _skill_when_to_use(form_dir: pathlib.Path) -> str | None:
    skill = form_dir / "SKILL.md"
    if not skill.exists():
        return None
    m = re.search(r"\*\*When to use:\*\*\s*(.+)",
                  skill.read_text(encoding="utf-8"))
    if not m:
        return None
    text = m.group(1).strip()
    return text[:397] + "..." if len(text) > 400 else text


def get_form_payload(form_id: str) -> dict:
    """Build the enriched, bounded (<~4KB) get_form response."""
    d = ROOT / "forms" / form_id
    if not (d / "mapping.json").exists():
        return {"error": f"unknown form {form_id!r}"}
    mapping = json.loads((d / "mapping.json").read_text(encoding="utf-8"))
    fields = mapping.get("fields", {})

    meta = {}
    meta_path = d / "form.yaml"
    if meta_path.exists():
        try:
            import yaml
            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        except Exception:
            meta = {}

    confidence: dict = {}
    unverified = []
    for key, spec in fields.items():
        level = spec.get("confidence") or "unknown"
        confidence[level] = confidence.get(level, 0) + 1
        if level != "high":
            unverified.append(key)
    unverified.sort()

    payload = {
        "form_id": form_id,
        "title": meta.get("title", form_id),
        "entity_type": meta.get("entity_type"),
        "statute": meta.get("statute"),
        "num_pages": meta.get("num_pages"),
        "when_to_use": _skill_when_to_use(d),
        "n_fields": len(fields),
        "trust": {
            "total_widgets": meta.get("num_fields"),
            "mapped_fields": meta.get("mapped_fields"),
            "confidence": confidence,
            "unverified_fields": unverified[:_MAX_UNVERIFIED],
            "note": ("fields below high confidence are unverified — tell "
                     "the user to check their placement"),
        },
        "fee": _catalog("fees.json").get("fees", {}).get(form_id),
        "workflows": _workflow_membership().get(form_id, []),
        "preflight": {
            "available": True,
            "hint": ("run the preflight tool (schema + rubric + signer "
                     "rules + coverage plan) before fill_form"),
        },
        "not_legal_advice": ("filled output is a draft; verify against the "
                             "official form before filing"),
    }
    if len(unverified) > _MAX_UNVERIFIED:
        payload["trust"]["unverified_fields_truncated"] = (
            len(unverified) - _MAX_UNVERIFIED)
    return payload


def find_forms_payload(situation: str, top_k: int = 5) -> list:
    """Route a situation, annotating each candidate with its workflows."""
    import route_form
    results, _ = route_form.route(situation, top_k)
    member = _workflow_membership()
    for r in results:
        r["workflows"] = [m["id"] for m in member.get(r.get("form_id"), [])]
    return results


def _fill(form_id: str, case: dict, out_dir: str, preflight) -> dict:
    """The repo fill path behind both fill tools (PreflightError keeps its
    machine-readable result instead of collapsing into the generic shape)."""
    from engine import fill as fill_engine
    from engine import preflight as preflight_engine

    out_path = pathlib.Path(out_dir) / f"{form_id}.filled.pdf"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        report: dict = {}
        out = fill_engine.fill(form_id, case, str(out_path), _FORMS_ROOT,
                               report=report, preflight=preflight)
        return {"ok": True, "path": str(out), "report": report}
    except preflight_engine.PreflightError as e:
        return {"ok": False, "error": "preflight blocked the fill",
                "preflight": e.result}


class Backend:
    """maine_forms_engine.mcp.FormsBackend for this repo."""

    name = "maine-corporation-forms"

    def find_forms(self, query: str, top_k: int = 5) -> list:
        """Route a free-text situation to candidate Maine SoS entity forms.

        Each candidate carries its ``workflows`` (multi-form bundle ids from
        catalog/workflows.json) so companion filings are not missed.
        """
        return find_forms_payload(query, top_k)

    def get_form(self, form_id: str) -> dict:
        """Return a form's metadata, trust/fee/workflow context, and hints.

        Includes the mapping trust summary (per-field confidence mix and the
        unverified below-high-confidence fields), the printed filing fee from
        catalog/fees.json (amount only when literally printed on the blank;
        null means see the SoS fee schedule), workflow membership (companion
        forms that must or may accompany this filing), a when-to-use excerpt
        from the form's SKILL.md, and preflight availability.
        """
        payload = get_form_payload(form_id)
        if "error" in payload:
            raise UnknownFormError(form_id)
        return payload

    def plan_fill(self, form_id: str, case: dict) -> dict:
        """Resolve a case object into the coverage plan (buckets)."""
        from engine import plan as plan_engine
        return plan_engine.build_plan(form_id, case, _FORMS_ROOT)

    def fill_form(self, form_id: str, case: dict, out_dir: str) -> dict:
        """Fill the form and write a PDF; returns {ok, path, report}.

        Preflight runs first and refuses on error-severity issues (use the
        ``fill_form_draft`` tool to fill a partial draft anyway). ``report``
        carries the fill diagnostics: preflight result, written,
        skipped_when, dropped_enums (enum values no option binding can
        place), and ignored_case_keys.
        """
        return _fill(form_id, case, out_dir, preflight=None)


def preflight(form_id: str, case: dict) -> dict:
    """Run every check (schema + rubric + signer rules + plan) at once.

    Returns one machine-readable issue list: {ok, issues, summary,
    coverage}. severity=error blocks fill_form by default;
    severity=manual entries are rubric checks that need human review.
    """
    from engine import preflight as preflight_engine
    return preflight_engine.preflight(form_id, case, _FORMS_ROOT)


def fill_form_draft(form_id: str, case: dict, out_dir: str) -> dict:
    """Fill WITHOUT the preflight gate (the old ``no_preflight=true``):
    writes a partial draft even when error-severity issues exist. Returns
    {ok, path, report}; the draft still needs every unresolved issue fixed
    before filing."""
    return _fill(form_id, case, out_dir, preflight="off")


EXTRA_TOOLS = (preflight, fill_form_draft)


def main():
    return _scaffold_main(Backend(), extra_tools=EXTRA_TOOLS)


if __name__ == "__main__":
    raise SystemExit(main())
