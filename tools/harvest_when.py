#!/usr/bin/env python3
"""Harvest machine-readable ``when`` conditions from rubric prose.

Each ``forms/<ID>/rubric.yaml`` check has a human-readable ``description`` and a
list of ``depends_on_keys``. A subset of those descriptions express a clean
conditional of the form

    "If <controller> is true, <target> must be ..."
    "If <controller> = 'value', <target> must be ..."

which is exactly a field-gating rule: ``<target>`` is *only applicable* when the
controller holds. This tool extracts that subset deterministically and writes a
``when`` expression onto the matching ``mapping.json`` field(s) for ``<target>``,
so the planner (``engine.plan``) can skip inapplicable fields.

It is intentionally conservative: only the two regular grammars above are
harvested. Multi-clause, "is set", set-membership, and format-only checks are
left alone (the planner keeps those fields surfaced). Idempotent — re-running
recomputes ``when`` from the rubric and rewrites only changed mappings.

    python3 tools/harvest_when.py            # write
    python3 tools/harvest_when.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# "If <ctrl> is true/false, <target> must ..."  (target = first dotted key after comma)
_RE_BOOL = re.compile(
    r"^if\s+([a-z0-9_.\[\]]+)\s+is\s+(true|false)\s*,\s*([a-z0-9_.\[\]]+)\b",
    re.I,
)
# "If <ctrl> = 'v' / == 'v', <target> must ..."
_RE_EQ = re.compile(
    r"^if\s+([a-z0-9_.\[\]]+)\s*(?:=|==)\s*'([^']+)'\s*,\s*([a-z0-9_.\[\]]+)\b",
    re.I,
)


def _schema_leaf(schema: dict, dotted: str):
    """Resolve a dotted canonical key to its schema leaf node, or None.

    Indices (``parties[0]`` / ``entities[*]``) are stripped before walking.
    """
    cur = schema.get("properties", {})
    node = None
    for part in re.sub(r"\[[^\]]*\]", "", dotted).split("."):
        if part not in cur:
            return None
        node = cur[part]
        cur = node.get("properties", {}) if node.get("type") == "object" else {}
    return node


def _controller_supports(schema: dict, ctrl: str, val: str) -> bool:
    """True if ``ctrl == val`` is verifiable against the schema.

    A boolean literal needs a boolean (or untyped) controller; any other
    literal must be a member of the controller's ``enum`` (untyped/enum-less
    controllers are accepted — there is nothing to contradict).
    """
    leaf = _schema_leaf(schema, ctrl)
    if leaf is None:
        return False
    if val in ("true", "false"):
        return leaf.get("type") in ("boolean", None)
    enum = leaf.get("enum")
    return enum is None or val in enum


def harvest_description(desc: str, schema: dict | None = None):
    """Return ``(target_key, when_expr)`` for a clean conditional, else None.

    When ``schema`` is given, a rule is dropped unless its controller/value is
    verifiable against the schema (the controller exists and, for non-boolean
    literals, the value is a real enum member). This keeps prose that
    abbreviates an enum value (e.g. ``'preexisted'`` for ``'merger_preexisted'``)
    from producing a ``when`` that can never be true.
    """
    d = (desc or "").strip()
    m = _RE_BOOL.match(d)
    if m:
        ctrl, val, target = m.group(1), m.group(2).lower(), m.group(3)
        if ctrl == target:
            return None
        if schema is not None and not _controller_supports(schema, ctrl, val):
            return None
        return target, f"{ctrl} == {val}"
    m = _RE_EQ.match(d)
    if m:
        ctrl, val, target = m.group(1), m.group(2), m.group(3)
        if ctrl == target:
            return None
        if schema is not None and not _controller_supports(schema, ctrl, val):
            return None
        return target, f"{ctrl} == '{val}'"
    return None


def harvest_form(form_dir: str):
    """Return ``{target_key: when_expr}`` harvested from one form's rubric."""
    rubric_path = os.path.join(form_dir, "rubric.yaml")
    if not os.path.exists(rubric_path):
        return {}
    with open(rubric_path, encoding="utf-8") as fh:
        rubric = yaml.safe_load(fh) or {}
    schema = {}
    schema_path = os.path.join(form_dir, "schema.json")
    if os.path.exists(schema_path):
        with open(schema_path, encoding="utf-8") as fh:
            schema = json.load(fh)
    when_by_key: dict[str, str] = {}
    for check in rubric.get("checks") or []:
        got = harvest_description(check.get("description", ""), schema)
        if not got:
            continue
        target, expr = got
        # Only honor a harvested target that the rubric itself lists as a
        # dependency (guards against the regex grabbing a stray token).
        deps = check.get("depends_on_keys") or []
        if target not in deps:
            continue
        # First writer wins; multiple checks rarely target the same key.
        when_by_key.setdefault(target, expr)
    return when_by_key


def apply_to_mapping(form_dir: str, when_by_key: dict, dry_run: bool):
    """Set ``when`` on matching mapping fields. Returns (set, cleared) counts."""
    mapping_path = os.path.join(form_dir, "mapping.json")
    if not os.path.exists(mapping_path):
        return 0, 0
    with open(mapping_path, encoding="utf-8") as fh:
        mapping = json.load(fh)
    fields = mapping.get("fields") or {}
    n_set = n_cleared = 0
    changed = False
    for key, spec in fields.items():
        desired = when_by_key.get(key)
        current = spec.get("when")
        if desired is not None:
            if current != desired:
                spec["when"] = desired
                changed = True
            n_set += 1
        elif current is not None:
            # Stale when from a previous run whose rubric no longer supports it.
            del spec["when"]
            changed = True
            n_cleared += 1
    if changed and not dry_run:
        with open(mapping_path, "w", encoding="utf-8") as fh:
            json.dump(mapping, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    return n_set, n_cleared


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--dry-run", action="store_true",
                    help="report harvest counts without writing mappings")
    ap.add_argument("--forms-root", default=os.path.join(ROOT, "forms"))
    a = ap.parse_args()

    total_when = total_set = total_cleared = forms_touched = 0
    unmatched_targets = []
    for form_dir in sorted(glob.glob(os.path.join(a.forms_root, "*"))):
        if not os.path.isdir(form_dir):
            continue
        when_by_key = harvest_form(form_dir)
        if when_by_key:
            total_when += len(when_by_key)
        n_set, n_cleared = apply_to_mapping(form_dir, when_by_key, a.dry_run)
        # Harvested keys that did not match any mapping field (reported, ignored).
        if when_by_key:
            mp = os.path.join(form_dir, "mapping.json")
            if os.path.exists(mp):
                mk = set(json.load(open(mp, encoding="utf-8")).get("fields", {}))
                for k in when_by_key:
                    if k not in mk:
                        unmatched_targets.append(
                            (os.path.basename(form_dir), k))
        if n_set or n_cleared:
            forms_touched += 1
        total_set += n_set
        total_cleared += n_cleared

    verb = "would set" if a.dry_run else "set"
    print(f"harvested {total_when} when-conditions from rubrics")
    print(f"{verb} `when` on {total_set} mapping fields across {forms_touched} "
          f"forms; cleared {total_cleared} stale")
    if unmatched_targets:
        print(f"NOTE {len(unmatched_targets)} harvested targets are not mapping "
              f"keys (ignored):")
        for f, k in unmatched_targets[:20]:
            print(f"  {f}: {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
