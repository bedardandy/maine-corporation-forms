"""Unified preflight: one machine-readable issue list for a (form, case).

The repo grew three validators with three output shapes — JSON-Schema
validation (``engine.schema``, error strings), signer rules
(``tools/signer_rules.py``, issue dicts), and the coverage plan
(``engine.plan``, buckets) — none of which called the others, and the
``rubric.yaml`` checks were never executed at all. ``preflight`` runs all
four and merges them into a single issue list::

    {
      "ok": bool,                    # no error-severity issue
      "form_id": ...,
      "issues": [{source, code, severity, keys, message, ...}, ...],
      "summary": {"error": n, "warning": n, "info": n, "manual": n},
      "coverage": {...},             # the plan's resolved/unresolved counts
    }

Issue ``source`` is one of ``schema`` / ``rubric`` / ``signer`` / ``plan``;
``severity`` is normalized to ``error`` / ``warning`` / ``info`` /
``manual`` (rubric checks that need human judgment — see engine.rubric).

``engine.fill`` runs preflight by default and refuses to write a PDF when an
error-severity issue is present (``--no-preflight`` / ``preflight="off"``
skips the gate; partial drafts are a legitimate use).

    python -m engine.preflight <FORM_ID> <case.json> [forms_root] [--json]
"""
import json
import sys
from pathlib import Path

from . import plan as plan_engine
from . import rubric as rubric_engine
from . import schema as schema_engine

_SIGNER_SEV = {"required": "error", "warning": "warning"}


def _signer_rules():
    """Import tools/signer_rules.py (tools/ is not a package)."""
    tools_dir = str(Path(__file__).resolve().parent.parent / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    import signer_rules
    return signer_rules


def preflight(form_id, case, forms_root="forms", today=None):
    """Run schema + rubric + signer + plan checks; return one issue list."""
    if not isinstance(case, dict):
        return {"ok": False, "form_id": form_id,
                "issues": [{"source": "schema", "code": "CASE_NOT_OBJECT",
                            "severity": "error", "keys": [],
                            "message": "case must be a JSON object (got "
                                       f"{type(case).__name__})"}],
                "summary": {"error": 1, "warning": 0, "info": 0,
                            "manual": 0},
                "coverage": None}

    issues = []

    # 1. JSON-Schema validation (types, enums, schema-required keys)
    schema_path = Path(forms_root) / form_id / "schema.json"
    if schema_path.exists():
        for err in schema_engine.validate(form_id, case, forms_root):
            issues.append({"source": "schema", "code": "SCHEMA_VALIDATION",
                           "severity": "error", "keys": [],
                           "message": err})

    # 2. rubric checks (executed where machine-checkable; MANUAL_REVIEW
    #    passthrough otherwise — see engine.rubric)
    rub = rubric_engine.evaluate(form_id, case, forms_root, today=today)
    rubric_error_keys = set()
    for i in rub["issues"]:
        issues.append({"source": "rubric", "code": i["code"],
                       "severity": i["severity"], "keys": i["keys"],
                       "message": i["message"],
                       "check_id": i["check_id"],
                       "rule_source": i["rule_source"]})
        if i["severity"] == "error":
            rubric_error_keys.update(i["keys"])

    # 3. signer rules (who may sign, in what capacity)
    try:
        signer_rules = _signer_rules()
        for i in signer_rules.validate(form_id, case, forms_root):
            issues.append({"source": "signer", "code": i["code"],
                           "severity": _SIGNER_SEV.get(i["severity"],
                                                       "warning"),
                           "keys": [], "message": i["message"]})
    except Exception as e:  # signer rules are advisory — never crash preflight
        issues.append({"source": "signer", "code": "SIGNER_RULES_UNAVAILABLE",
                       "severity": "warning", "keys": [],
                       "message": f"signer validation skipped: "
                                  f"{type(e).__name__}: {e}"})

    # 4. coverage plan (when-gates, required facts, undeliverable enums)
    coverage = None
    p = plan_engine.build_plan(form_id, case, forms_root)
    if not p.get("ok"):
        issues.append({"source": "plan", "code": "PLAN_FAILED",
                       "severity": "error", "keys": [],
                       "message": p.get("error", "plan failed")})
    else:
        coverage = p["coverage"]
        for u in p["unresolved"]:
            if not u["required"]:
                continue
            # The rubric *evaluates* required logic (including conditionals)
            # and already errors on real gaps; the plan's flag is the cruder
            # "referenced by a required check" approximation (it flags e.g.
            # multi_class_exhibit_letter on a single-class corporation), so
            # it surfaces as a warning, never a block.
            if u["key"] in rubric_error_keys:
                continue
            issues.append({"source": "plan", "code": "MISSING_REQUIRED_FACT",
                           "severity": "warning", "keys": [u["key"]],
                           "message": f"{u['key']} ({u['label']}) is "
                                      "referenced by a required rubric check "
                                      "but has no value — confirm it is not "
                                      "applicable to this case"})
        for ue in p["unmapped_enums"]:
            issues.append({"source": "plan", "code": "UNMAPPED_ENUM",
                           "severity": "error", "keys": [ue["key"]],
                           "message": f"{ue['key']} = {ue['value']!r} maps "
                                      "to no option (allowed: "
                                      + ", ".join(ue["allowed"]) + ") — it "
                                      "would be silently undeliverable at "
                                      "fill time"})

    summary = {"error": 0, "warning": 0, "info": 0, "manual": 0}
    for i in issues:
        summary[i["severity"]] = summary.get(i["severity"], 0) + 1

    return {
        "ok": summary["error"] == 0,
        "form_id": form_id,
        "issues": issues,
        "summary": summary,
        "coverage": coverage,
        "note": ("Not legal advice. severity=error blocks engine.fill by "
                 "default (override with --no-preflight); manual entries "
                 "are rubric checks that need human judgment and must be "
                 "reviewed, not ignored."),
    }


class PreflightError(Exception):
    """Raised by engine.fill when preflight finds error-severity issues."""

    def __init__(self, result):
        self.result = result
        errors = [i for i in result["issues"] if i["severity"] == "error"]
        lines = [f"preflight found {len(errors)} blocking issue(s) for "
                 f"{result['form_id']} (use --no-preflight / "
                 "preflight=\"off\" to fill a partial draft):"]
        for i in errors[:10]:
            lines.append(f"  [{i['source']}/{i['code']}] {i['message']}")
        if len(errors) > 10:
            lines.append(f"  ... and {len(errors) - 10} more")
        super().__init__("\n".join(lines))


def _cli(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print("usage: python -m engine.preflight <FORM_ID> <case.json> "
              "[forms_root] [--json]")
        return 2
    form_id, case_path = args[0], args[1]
    forms_root = args[2] if len(args) > 2 else "forms"
    case = json.loads(Path(case_path).read_text(encoding="utf-8"))
    result = preflight(form_id, case, forms_root)
    if "--json" in argv:
        print(json.dumps(result, indent=2))
    else:
        s = result["summary"]
        print(f"{result['form_id']}: {'OK' if result['ok'] else 'BLOCKED'} — "
              f"{s['error']} error(s), {s['warning']} warning(s), "
              f"{s['info']} info, {s['manual']} manual-review")
        for i in result["issues"]:
            if i["severity"] == "manual":
                continue
            print(f"  {i['severity'].upper():7s} [{i['source']}/{i['code']}] "
                  f"{i['message']}")
        n_manual = s["manual"]
        if n_manual:
            print(f"  MANUAL  {n_manual} rubric check(s) need human review "
                  "(--json lists them)")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
