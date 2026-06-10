#!/usr/bin/env python3
"""MCP server exposing the Maine SoS corporation-forms library to agents.

Tools (stdio, FastMCP):
  find_forms(situation, top_k=5)        -> candidate forms (router), each
                                           annotated with workflow membership
  get_form(form_id)                     -> metadata + trust summary (per-field
                                           confidence), printed filing fee,
                                           workflows, SKILL.md excerpt
  plan_fill(form_id, case)              -> coverage plan (resolved/unresolved/skipped)
  fill_form(form_id, case, out_path)    -> write a filled PDF, return {ok, path}

Run:      python3 tools/agent_server.py
Register: claude mcp add maine-corporation-forms -- python3 tools/agent_server.py

Requires ``mcp`` (pip install mcp). The import is lazy so the module documents
itself even without the dependency installed.
"""
from __future__ import annotations

import functools
import json
import pathlib
import re
import sys

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


def _build():
    from mcp.server.fastmcp import FastMCP

    from engine import fill as fill_engine
    from engine import plan as plan_engine
    from engine import preflight as preflight_engine

    mcp = FastMCP("maine-corporation-forms")

    @mcp.tool()
    def find_forms(situation: str, top_k: int = 5) -> list:
        """Route a free-text situation to candidate Maine SoS entity forms.

        Each candidate carries its ``workflows`` (multi-form bundle ids from
        catalog/workflows.json) so companion filings are not missed.
        """
        return find_forms_payload(situation, top_k)

    @mcp.tool()
    def get_form(form_id: str) -> dict:
        """Return a form's metadata, trust/fee/workflow context, and hints.

        Includes the mapping trust summary (per-field confidence mix and the
        unverified below-high-confidence fields), the printed filing fee from
        catalog/fees.json (amount only when literally printed on the blank;
        null means see the SoS fee schedule), workflow membership (companion
        forms that must or may accompany this filing), a when-to-use excerpt
        from the form's SKILL.md, and preflight availability.
        """
        return get_form_payload(form_id)

    @mcp.tool()
    def plan_fill(form_id: str, case: dict) -> dict:
        """Resolve a case object into the coverage plan (buckets)."""
        return plan_engine.build_plan(form_id, case, _FORMS_ROOT)

    @mcp.tool()
    def preflight(form_id: str, case: dict) -> dict:
        """Run every check (schema + rubric + signer rules + plan) at once.

        Returns one machine-readable issue list: {ok, issues, summary,
        coverage}. severity=error blocks fill_form by default;
        severity=manual entries are rubric checks that need human review.
        """
        return preflight_engine.preflight(form_id, case, _FORMS_ROOT)

    @mcp.tool()
    def fill_form(form_id: str, case: dict, out_path: str,
                  no_preflight: bool = False) -> dict:
        """Fill the form and write a PDF; returns {ok, path, report}.

        Preflight runs first and refuses on error-severity issues (set
        ``no_preflight=true`` to fill a partial draft anyway). ``report``
        carries the fill diagnostics: preflight result, written,
        skipped_when, dropped_enums (enum values no option binding can
        place), and ignored_case_keys.
        """
        try:
            report: dict = {}
            out = fill_engine.fill(form_id, case, out_path, _FORMS_ROOT,
                                   report=report,
                                   preflight="off" if no_preflight
                                   else None)
            return {"ok": True, "path": str(out), "report": report}
        except preflight_engine.PreflightError as e:
            return {"ok": False, "error": "preflight blocked the fill",
                    "preflight": e.result}
        except Exception as e:
            return {"ok": False, "error": f"{type(e).__name__}: {e}"}

    return mcp


def main():
    try:
        mcp = _build()
    except ImportError:
        print("mcp not installed: pip install mcp", file=sys.stderr)
        return 1
    mcp.run()  # stdio transport
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
