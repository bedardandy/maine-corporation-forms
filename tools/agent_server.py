#!/usr/bin/env python3
"""MCP server exposing the Maine SoS corporation-forms library to agents.

Tools (stdio, FastMCP):
  find_forms(situation, top_k=5)        -> candidate forms (router)
  get_form(form_id)                     -> metadata + field summary
  plan_fill(form_id, case)              -> coverage plan (resolved/unresolved/skipped)
  fill_form(form_id, case, out_path)    -> write a filled PDF, return {ok, path}

Run:      python3 tools/agent_server.py
Register: claude mcp add maine-corporation-forms -- python3 tools/agent_server.py

Requires ``mcp`` (pip install mcp). The import is lazy so the module documents
itself even without the dependency installed.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

_FORMS_ROOT = str(ROOT / "forms")


def _build():
    from mcp.server.fastmcp import FastMCP

    import route_form
    from engine import fill as fill_engine
    from engine import plan as plan_engine

    mcp = FastMCP("maine-corporation-forms")

    @mcp.tool()
    def find_forms(situation: str, top_k: int = 5) -> list:
        """Route a free-text situation to candidate Maine SoS entity forms."""
        results, _ = route_form.route(situation, top_k)
        return results

    @mcp.tool()
    def get_form(form_id: str) -> dict:
        """Return a form's metadata and a compact field summary."""
        d = ROOT / "forms" / form_id
        if not (d / "mapping.json").exists():
            return {"error": f"unknown form {form_id!r}"}
        mapping = json.loads((d / "mapping.json").read_text())
        title = form_id
        meta = d / "form.yaml"
        if meta.exists():
            try:
                import yaml
                title = (yaml.safe_load(meta.read_text()) or {}).get(
                    "title", form_id)
            except Exception:
                pass
        return {"form_id": form_id, "title": title,
                "n_fields": len(mapping.get("fields", {}))}

    @mcp.tool()
    def plan_fill(form_id: str, case: dict) -> dict:
        """Resolve a case object into the coverage plan (buckets)."""
        return plan_engine.build_plan(form_id, case, _FORMS_ROOT)

    @mcp.tool()
    def fill_form(form_id: str, case: dict, out_path: str) -> dict:
        """Fill the form and write a PDF; returns {ok, path, report}.

        ``report`` carries the fill diagnostics: written, skipped_when,
        dropped_enums (enum values no option binding can place), and
        ignored_case_keys.
        """
        try:
            report: dict = {}
            out = fill_engine.fill(form_id, case, out_path, _FORMS_ROOT,
                                   report=report)
            return {"ok": True, "path": str(out), "report": report}
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
