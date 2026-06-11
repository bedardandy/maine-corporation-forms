"""Audit per-form README mechanical claims against the live mapping.json.

The per-form READMEs were emitted once by tools/build_from_pass1.py and then
hand-extended ("Open question:" / "Resolved:" notes). The *mechanical* lines
— claims that are fully derivable from mapping.json — go stale whenever a
remap round changes bindings (e.g. the button-binding sweeps that split
``filing.expedited_service`` into three independent checkbox sub-keys).

Checked claim classes (everything else in a README is left alone):

1. Fan-out claim (generator boilerplate, "Known ambiguities" section):
       - `<key>` maps to N widgets; all receive the same value.
   Verified against the canonical-key view of mapping.json
   (engine.mapping.entries): valid only if <key> still binds as a
   multi-widget fan-out (``widget_id`` list) of exactly N widgets.
2. Low-confidence claim (generator boilerplate, same section):
       - N low-confidence mapping(s) need human review: `k1`, `k2` ...
   Recomputed from the bindings' ``confidence`` fields, rendered in the
   generator's exact format (first 6 keys, " ..." overflow). Dropped when no
   low-confidence binding remains.
3. Header count:
       **Mapped fields:** N
   The generator defined this as the number of canonical entries
   (``len(mapping["fields"])``); recomputed as ``len(entries(mapping))``.

Replacement text is derived from mapping.json data only (key names,
field_type, widget counts, option names) — never invented prose.

Anything the auditor cannot mechanically prove stale (e.g. a fan-out claim
whose key vanished without successor sub-keys, or hand-written notes that
reference keys absent from mapping.json) is *reported*, never edited.

Usage:
    python3 tools/audit_readme_claims.py            # report; exit 1 if stale
    python3 tools/audit_readme_claims.py --fix      # rewrite stale lines
    python3 tools/audit_readme_claims.py FORM_ID... # restrict to some forms
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.mapping import ENUM_GROUP_TYPES, entries as mapping_entries  # noqa: E402

FORMS = ROOT / "forms"

FANOUT_RE = re.compile(
    r"^- `(?P<key>[^`]+)` maps to (?P<n>\d+) widgets; "
    r"all receive the same value\.$")
LOWCONF_RE = re.compile(
    r"^- \d+ low-confidence mapping\(s\) need human review: .+$")
MAPPED_RE = re.compile(r"^(?P<head>\*\*Mapped fields:\*\* )\d+(?P<tail>\s*)$")
# backticked tokens shaped like canonical keys (dotted / indexed paths)
KEYREF_RE = re.compile(
    r"`([a-z][a-z0-9_]*(?:\.[a-z0-9_]+|\[\d+\])+(?:\.\*)?)`")

AMBIG_HEADER = "## Known ambiguities"


def render_lowconf(low_keys):
    """The generator's exact low-confidence line (build_from_pass1.py)."""
    return ("- " + f"{len(low_keys)} low-confidence mapping(s) need human "
            "review: " + ", ".join(f"`{k}`" for k in low_keys[:6])
            + (" ..." if len(low_keys) > 6 else ""))


def fanout_verdict(key, claimed_n, ents):
    """Check one fan-out claim. Returns (status, replacement_or_reason).

    status: "ok" (claim still true), "fix" (replacement line proven from
    mapping.json), or "ambiguous" (stale but no mechanical replacement).
    """
    if key in ents:
        spec = ents[key]
        ftype = spec.get("field_type") or "text"
        wid = spec.get("widget_id")
        if isinstance(wid, list):
            if len(wid) == claimed_n:
                return "ok", None
            return "fix", (f"- `{key}` maps to {len(wid)} widgets; "
                           "all receive the same value.")
        options = spec.get("options") or {}
        if ftype in ENUM_GROUP_TYPES:
            n_widgets = len(set(options.values()))
            return "fix", (
                f"- `{key}` binds as a single {ftype} selecting among "
                f"{n_widgets} option widgets (accepted values: "
                f"{', '.join(options)}).")
        if ftype == "radio" and options:
            return "fix", (
                f"- `{key}` binds as a single radio group `{wid}` with "
                f"{len(options)} options ({', '.join(options)}).")
        return "fix", f"- `{key}` maps to a single {ftype} widget (`{wid}`)."
    subs = {k: s for k, s in ents.items() if k.startswith(key + ".")}
    if subs:
        if all((s.get("field_type") == "checkbox"
                and not isinstance(s.get("widget_id"), list))
               for s in subs.values()):
            leaves = [k[len(key) + 1:] for k in subs]
            return "fix", (
                f"- `{key}.*` maps to {len(subs)} independent boolean "
                f"checkboxes ({', '.join(leaves)}).")
        parts = "; ".join(
            f"`{k}` ({s.get('field_type') or 'text'})"
            for k, s in subs.items())
        return "fix", (f"- `{key}` is split into {len(subs)} independent "
                       f"sub-keys: {parts}.")
    return "ambiguous", (f"key `{key}` is gone from mapping.json and has no "
                         "successor sub-keys; no mechanical replacement")


def key_exists(token, ents):
    """Loose existence check for hand-written key references (report-only)."""
    base = token[:-2] if token.endswith(".*") else token
    if base in ents:
        return True
    prefix = base + "."
    return any(k.startswith(prefix) for k in ents)


def audit_form(form_dir, fix=False):
    """Audit (and optionally fix) one form. Returns a result dict."""
    res = {"form_id": form_dir.name, "checked": 0, "ok": 0,
           "fixed": [], "stale": [], "ambiguous": [], "missing_key_refs": []}
    readme = form_dir / "README.md"
    mapping_path = form_dir / "mapping.json"
    if not readme.exists() or not mapping_path.exists():
        return res
    ents = mapping_entries(json.loads(mapping_path.read_text(encoding="utf-8")))
    low_keys = [k for k, s in ents.items() if s.get("confidence") == "low"]

    lines = readme.read_text(encoding="utf-8").splitlines()
    out = []
    in_ambig = False
    changed = False
    for line in lines:
        if line.startswith("## "):
            in_ambig = line.strip() == AMBIG_HEADER

        m = MAPPED_RE.match(line)
        if m:
            res["checked"] += 1
            expected = f"{m.group('head')}{len(ents)}{m.group('tail')}"
            if line == expected:
                res["ok"] += 1
            elif fix:
                res["fixed"].append((line.strip(), expected.strip()))
                line = expected
                changed = True
            else:
                res["stale"].append((line.strip(), expected.strip()))
            out.append(line)
            continue

        if in_ambig:
            m = FANOUT_RE.match(line)
            if m:
                res["checked"] += 1
                status, repl = fanout_verdict(
                    m.group("key"), int(m.group("n")), ents)
                if status == "ok":
                    res["ok"] += 1
                elif status == "fix":
                    if fix:
                        res["fixed"].append((line, repl))
                        line = repl
                        changed = True
                    else:
                        res["stale"].append((line, repl))
                else:
                    res["ambiguous"].append((line, repl))
                out.append(line)
                continue
            if LOWCONF_RE.match(line):
                res["checked"] += 1
                expected = render_lowconf(low_keys) if low_keys else None
                if line == expected:
                    res["ok"] += 1
                elif fix:
                    res["fixed"].append((line, expected or "<removed>"))
                    changed = True
                    if expected is not None:
                        out.append(expected)
                    continue
                else:
                    res["stale"].append((line, expected or "<removed>"))
                out.append(line)
                continue
            # hand-written note: report (never edit) dangling key references
            for token in KEYREF_RE.findall(line):
                if not key_exists(token, ents):
                    res["missing_key_refs"].append(token)
            out.append(line)
            continue

        out.append(line)

    if fix and changed:
        readme.write_text("\n".join(out) + "\n", encoding="utf-8")
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("form_ids", nargs="*",
                    help="restrict to these form ids (default: all)")
    ap.add_argument("--fix", action="store_true",
                    help="rewrite provably-stale lines in place")
    ap.add_argument("--quiet", action="store_true",
                    help="only print the summary and problems")
    args = ap.parse_args(argv)

    form_dirs = ([FORMS / f for f in args.form_ids] if args.form_ids
                 else sorted(p for p in FORMS.iterdir() if p.is_dir()))
    totals = {"forms": 0, "checked": 0, "ok": 0, "fixed": 0, "stale": 0}
    ambiguous, missing_refs = [], []
    for form_dir in form_dirs:
        res = audit_form(form_dir, fix=args.fix)
        totals["forms"] += 1
        totals["checked"] += res["checked"]
        totals["ok"] += res["ok"]
        totals["fixed"] += len(res["fixed"])
        totals["stale"] += len(res["stale"])
        for old, new in res["fixed"]:
            if not args.quiet:
                print(f"FIXED {res['form_id']}:\n  - {old}\n  + {new}")
        for old, new in res["stale"]:
            print(f"STALE {res['form_id']}:\n  - {old}\n  + {new}")
        for old, why in res["ambiguous"]:
            ambiguous.append((res["form_id"], old, why))
        for tok in res["missing_key_refs"]:
            missing_refs.append((res["form_id"], tok))

    for form_id, old, why in ambiguous:
        print(f"AMBIGUOUS {form_id}: {old}\n  ({why})")
    for form_id, tok in missing_refs:
        print(f"NOTE {form_id}: hand-written note references `{tok}` "
              "which is not in mapping.json (report-only)")
    print(f"\n{totals['forms']} forms scanned, {totals['checked']} mechanical "
          f"claims checked: {totals['ok']} valid, {totals['fixed']} fixed, "
          f"{totals['stale']} stale, {len(ambiguous)} ambiguous (untouched), "
          f"{len(missing_refs)} dangling hand-written key references "
          "(report-only).")
    return 1 if totals["stale"] else 0


if __name__ == "__main__":
    sys.exit(main())
