#!/usr/bin/env python3
"""Adversarial fuzz harness over every form's plan + fill path.

Exercises all 156 forms against a battery of hostile case shapes and asserts the
library degrades cleanly instead of crashing or silently corrupting:

  - empty / all-null / non-dict top-level case
  - type-fuzz values (lists, ints, bools, nested dicts, huge strings,
    unicode + control chars) on real canonical keys
  - the shipped example cases (happy path)

For each it checks: plan() never raises and its buckets partition n_fields;
plan() rejects a non-dict case with a clean error; fill() never raises and emits
a valid ``%PDF`` byte stream. Reports findings; exit non-zero if any are real.

    python3 tools/fuzz.py            # summary
    python3 tools/fuzz.py --verbose  # per-finding detail
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(ROOT))

from engine import fill as fill_engine  # noqa: E402
from engine import plan as plan_engine  # noqa: E402

_FORMS_ROOT = str(ROOT / "forms")

# Hostile values stamped onto a few real top-level keys.
_FUZZ_VALUES = [
    [],
    {},
    [1, 2, 3],
    {"nested": {"deep": True}},
    12345,
    True,
    False,
    None,
    "x" * 5000,
    "üñîçödé \t\n\x00 control",
    "'; DROP TABLE forms; --",
    "<script>alert(1)</script>",
]


def _form_ids():
    return sorted(p.name for p in (ROOT / "forms").iterdir()
                  if p.is_dir() and (p / "mapping.json").exists())


def _fuzz_cases(form_id):
    """Yield (label, case) hostile inputs for a form."""
    yield "empty", {}
    yield "all-null", {"entity": None, "clerk": None, "filing": None}
    yield "non-dict-list", [1, 2, 3]
    yield "non-dict-str", "not a case"
    yield "non-dict-null", None
    # type-fuzz: stamp each hostile value on entity (a key every form has)
    for i, v in enumerate(_FUZZ_VALUES):
        yield f"typefuzz-entity-{i}", {"entity": v}
        yield f"typefuzz-name-{i}", {"entity": {"name": v}}


def _check_plan(form_id, label, case, findings):
    try:
        p = plan_engine.build_plan(form_id, case, _FORMS_ROOT)
    except Exception as e:
        findings.append((form_id, label, "plan-crash", f"{type(e).__name__}: {e}"))
        return
    if not isinstance(case, dict):
        if p.get("ok") is not False:
            findings.append((form_id, label, "plan-accepted-nondict",
                             "non-dict case should return ok=False"))
        return
    if not p.get("ok"):
        findings.append((form_id, label, "plan-not-ok", p.get("error", "")))
        return
    c = p["coverage"]
    if c["resolved"] + c["unresolved"] + c["skipped"] != p["n_fields"]:
        findings.append((form_id, label, "plan-partition",
                         f"{c} != n_fields={p['n_fields']}"))


def _check_fill(form_id, label, case, findings):
    if not isinstance(case, dict):
        return  # fill is only defined for dict cases
    try:
        buf = io.BytesIO()
        fill_engine.fill_to_stream(form_id, case, buf, _FORMS_ROOT)
    except Exception as e:
        findings.append((form_id, label, "fill-crash", f"{type(e).__name__}: {e}"))
        return
    data = buf.getvalue()
    if not data.startswith(b"%PDF-"):
        findings.append((form_id, label, "fill-not-pdf",
                         f"first bytes {data[:8]!r}"))


def _check_examples(findings):
    for ex in sorted(glob.glob(str(ROOT / "examples" / "*.case.json"))):
        name = pathlib.Path(ex).stem  # e.g. corp_mbca-6.case
        form_id = None
        stem = name[:-5] if name.endswith(".case") else name
        # match example stem to a form_id case-insensitively
        for fid in _form_ids():
            if fid.lower() == stem.lower():
                form_id = fid
                break
        if form_id is None:
            findings.append((stem, "example", "no-matching-form",
                             f"{ex} has no form dir"))
            continue
        case = json.loads(pathlib.Path(ex).read_text())
        _check_plan(form_id, "example", case, findings)
        _check_fill(form_id, "example", case, findings)


def run():
    findings = []
    forms = _form_ids()
    for form_id in forms:
        for label, case in _fuzz_cases(form_id):
            _check_plan(form_id, label, case, findings)
            _check_fill(form_id, label, case, findings)
    _check_examples(findings)
    return forms, findings


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    forms, findings = run()
    n_cases = len(forms) * len(list(_fuzz_cases("CORP_MBCA-6")))
    print(f"fuzzed {len(forms)} forms x {len(list(_fuzz_cases('CORP_MBCA-6')))} "
          f"shapes = ~{n_cases} plan/fill runs + examples")
    if not findings:
        print("0 findings — all forms degrade cleanly")
        return 0
    print(f"{len(findings)} findings:")
    by_kind = {}
    for f in findings:
        by_kind.setdefault(f[2], 0)
        by_kind[f[2]] += 1
    for kind, n in sorted(by_kind.items()):
        print(f"  {kind}: {n}")
    if a.verbose:
        for fid, label, kind, detail in findings:
            print(f"  [{kind}] {fid} ({label}): {detail}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
