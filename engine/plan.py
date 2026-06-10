"""Resolve a form's mapping against a case object into a *fill plan*.

Where :mod:`engine.fill` writes the PDF, this reports — without touching a PDF —
which canonical keys a case object satisfies, which are missing, and which are
*not applicable* because a ``when`` condition gates them off. It is the
auditable companion to ``fill``: an integrator can show a user the coverage
before committing a filing.

Each ``forms/<ID>/mapping.json`` field is sorted into:

- ``resolved``   — the canonical key resolves to a non-empty value.
- ``unresolved`` — the key has no value in the case (a missing fact to collect).
                   Flagged ``required`` when a ``rubric.yaml`` check of
                   ``severity: required`` depends on it.
- ``skipped``    — the field's ``when`` condition is definitively false for this
                   case (e.g. a commercial-agent CRA number when the agent is
                   noncommercial), so it is not applicable.

Gating is conservative: a field is skipped only when its ``when`` controller is
*known* and the condition is false. An unknown controller leaves the field in
its normal bucket — the safe default for legal forms.

``when`` is harvested from rubric prose by ``tools/harvest_when.py``; its grammar
is ``LHS == v`` / ``LHS != v`` / ``LHS == true|false`` / ``LHS in ['a','b']`` /
bare ``LHS`` (truthy), where ``LHS`` is a dotted canonical key.

    python -m engine.plan CORP_MBCA-6 case.json
"""
import json
import re
import sys
from pathlib import Path

from . import canonical

_TRUTHY = {"yes", "true", "1", "on", "y", "checked"}
_FALSY = {"no", "false", "0", "off", "n", "", "none", "unchecked"}


def _truthy(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    if isinstance(v, (int, float)):
        return v != 0
    if isinstance(v, (list, tuple, set, dict)):
        return len(v) > 0
    s = str(v).strip().lower()
    if s in _TRUTHY:
        return True
    if s in _FALSY:
        return False
    return bool(s)


def _unquote(tok):
    tok = tok.strip()
    if len(tok) >= 2 and tok[0] in "'\"" and tok[-1] == tok[0]:
        return tok[1:-1]
    return tok


def _scalar_eq(val, token):
    if isinstance(val, (list, tuple, set)):
        return any(_scalar_eq(x, token) for x in val)
    t = token.strip().lower()
    if t in ("true", "false", "yes", "no"):
        return _truthy(val) == (t in ("true", "yes"))
    return str(val).strip().lower() == t


def eval_when(expr, case):
    """Evaluate a ``when`` expression against a case object.

    Returns True (applies), False (gate off), or None (controller unknown).
    Controllers are resolved as dotted canonical keys via :mod:`engine.canonical`.
    """
    expr = (expr or "").strip()
    m = re.match(r"^([A-Za-z0-9_.\[\]]+)\s+in\s+\[(.*)\]$", expr)
    if m:
        lhs, items = m.group(1), m.group(2)
        v = canonical.get(case, lhs)
        if v in (None, ""):
            return None
        opts = [_unquote(x).lower() for x in items.split(",") if x.strip()]
        if isinstance(v, (list, tuple, set)):
            return any(str(x).strip().lower() in opts for x in v)
        return str(v).strip().lower() in opts
    m = re.match(r"^([A-Za-z0-9_.\[\]]+)\s*(==|!=)\s*(.+?)$", expr)
    if m:
        lhs, op, rhs = m.group(1), m.group(2), _unquote(m.group(3))
        v = canonical.get(case, lhs)
        if v in (None, ""):
            return None
        hit = _scalar_eq(v, rhs)
        return hit if op == "==" else (not hit)
    m = re.match(r"^([A-Za-z0-9_.\[\]]+)$", expr)
    if m:
        v = canonical.get(case, expr)
        if v in (None, ""):
            return None
        return _truthy(v)
    return None


def _required_keys(form_id, forms_root):
    """Canonical keys named by a ``severity: required`` rubric check."""
    path = Path(forms_root) / form_id / "rubric.yaml"
    if not path.exists():
        return set()
    try:
        import yaml
    except ImportError:
        return set()
    rubric = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    keys = set()
    for check in rubric.get("checks") or []:
        if check.get("severity") == "required":
            keys.update(check.get("depends_on_keys") or [])
    return keys


def _is_empty(value):
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0
    return False


def build_plan(form_id, case, forms_root="forms"):
    """Return a coverage plan for ``form_id`` against ``case`` (a nested dict)."""
    if not isinstance(case, dict):
        return {"ok": False, "error": f"case must be a JSON object (got "
                f"{type(case).__name__})"}
    mapping_path = Path(forms_root) / form_id / "mapping.json"
    if not mapping_path.exists():
        return {"ok": False, "error": f"unknown form {form_id!r} "
                f"(no {mapping_path})"}
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    fields = mapping.get("fields") or {}
    required = _required_keys(form_id, forms_root)

    resolved, unresolved, skipped = {}, [], []
    unmapped_enums = []
    for key, spec in fields.items():
        label = spec.get("label", key)
        # An entry may resolve a different canonical key than its dict key
        # (two when-gated entries feeding one key; see engine.fill docstring).
        ckey = spec.get("canonical_key", key)
        when = spec.get("when")
        if when is not None and eval_when(when, case) is False:
            skipped.append({"key": key, "label": label, "when": when})
            continue
        value = canonical.get(case, ckey)
        if _is_empty(value):
            unresolved.append({"key": ckey, "label": label,
                               "required": ckey in required})
        else:
            resolved[key] = value
            # A resolved enum value that maps to no option would be silently
            # undeliverable at fill time — surface it here too.
            if spec.get("field_type") in ("radio", "enum_select",
                                          "enum_text_select"):
                options = spec.get("options") or {}
                if options and str(value) not in options:
                    unmapped_enums.append({"key": key, "value": str(value),
                                           "allowed": sorted(options)})

    return {
        "ok": True,
        "form_id": form_id,
        "n_fields": len(fields),
        "resolved": resolved,
        "unresolved": unresolved,
        "skipped": skipped,
        "unmapped_enums": unmapped_enums,
        "coverage": {
            "resolved": len(resolved),
            "unresolved": len(unresolved),
            "unresolved_required": sum(1 for u in unresolved if u["required"]),
            "skipped": len(skipped),
        },
        "note": ("Not legal advice. `unresolved` are missing facts to collect "
                 "(`required: true` are blocking per the rubric); `skipped` "
                 "fields are gated off by a `when` condition and not applicable "
                 "to this case; `unmapped_enums` are enum values no option "
                 "binding can place. Write the filled PDF with engine.fill."),
    }


def _cli(argv):
    if len(argv) < 3:
        print("usage: python -m engine.plan <FORM_ID> <case.json> [forms_root] "
              "[--full]")
        return 1
    form_id = argv[1]
    case = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    forms_root = "forms"
    full = "--full" in argv
    for a in argv[3:]:
        if a != "--full":
            forms_root = a
    plan = build_plan(form_id, case, forms_root)
    if not plan["ok"]:
        print(plan["error"])
        return 1
    if full:
        print(json.dumps(plan, indent=2))
        return 0
    c = plan["coverage"]
    print(f"{plan['form_id']}: {plan['n_fields']} fields — "
          f"resolved {c['resolved']}, unresolved {c['unresolved']} "
          f"({c['unresolved_required']} required), skipped {c['skipped']}")
    for u in plan["unresolved"]:
        if u["required"]:
            print(f"  MISSING (required): {u['key']}")
    for s in plan["skipped"]:
        print(f"  skipped: {s['key']} (when {s['when']})")
    for u in plan["unmapped_enums"]:
        print(f"  UNMAPPED ENUM: {u['key']} = {u['value']!r} "
              f"(allowed: {', '.join(u['allowed'])})")
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
