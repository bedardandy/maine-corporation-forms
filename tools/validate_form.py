"""Validate a form folder without a PDF — the modular-improvement inner loop.

Checks one form (or all) for internal consistency between its ``mapping.json``,
``schema.json``, ``fields.csv``, and ``rubric.yaml``. It needs no blank PDF and
no network, so it runs offline and in CI.

Two severities:

- **error** — structural breakage that makes the folder unusable: a file that
  does not parse, or a mapping field missing ``widget_id`` / ``field_type``.
  Any error makes the run exit non-zero (the CI gate).
- **review** — a finding to look at before trusting the form: a ``widget_id``
  the captured ``fields.csv`` inventory does not list (often a form the state
  has revised since capture — ``mapping.json`` is authoritative there), a
  canonical key not yet defined in ``schema.json``, a ``low`` confidence field,
  or a ``when`` expression outside the supported grammar. Reviews never fail the
  run; they are the per-form worklist.

    python3 tools/validate_form.py CORP_MBCA-6      # one form
    python3 tools/validate_form.py --all            # every form, summary
    python3 tools/validate_form.py --all --json     # machine-readable
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.mapping import entries as mapping_entries  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "forms"

# Supported `when` grammar (mirrors engine.plan.eval_when).
_WHEN_RE = [
    re.compile(r"^[A-Za-z0-9_.\[\]]+\s+in\s+\[.*\]$"),
    re.compile(r"^[A-Za-z0-9_.\[\]]+\s*(==|!=)\s*.+$"),
    re.compile(r"^[A-Za-z0-9_.\[\]]+$"),
]


def _well_formed_when(expr):
    expr = (expr or "").strip()
    return any(r.match(expr) for r in _WHEN_RE)


def _schema_has(schema, dotted):
    node = schema
    for part in dotted.split("."):
        part = re.sub(r"\[\d+\]$", "", part)
        props = node.get("properties") if isinstance(node, dict) else None
        if not props or part not in props:
            return False
        node = props[part]
        if node.get("type") == "array" and "items" in node:
            node = node["items"]
    return True


def _widget_inventory(form_dir):
    ids = set()
    fc = form_dir / "fields.csv"
    if not fc.exists():
        return None
    with open(fc, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("widget_id"):
                ids.add(row["widget_id"])
    return ids


def validate_form(form_id):
    """Return ``{form_id, errors, reviews, stats}`` for one form."""
    d = FORMS / form_id
    errors, reviews = [], []

    def _load(name, loader):
        p = d / name
        if not p.exists():
            errors.append(f"missing {name}")
            return None
        try:
            return loader(p.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            errors.append(f"{name} does not parse: {exc}")
            return None

    mapping = _load("mapping.json", json.loads)
    schema = _load("schema.json", json.loads)
    _load("form.yaml", lambda t: t)  # presence + readability only
    inventory = _widget_inventory(d)
    if inventory is None:
        errors.append("missing fields.csv")

    stats = {"fields": 0, "high": 0, "medium": 0, "low": 0, "when_gated": 0}
    if mapping is not None:
        try:
            fields = mapping_entries(mapping)
        except ValueError as exc:
            # e.g. a legacy canonical-key-keyed mapping.json — direction drift
            errors.append(f"mapping.json: {exc}")
            fields = {}
        stats["fields"] = len(fields)
        if not fields:
            reviews.append("no mapped fields (flat / reference document, or "
                           "not yet mapped)")
        for key, spec in fields.items():
            if not isinstance(spec, dict):
                errors.append(f"field {key!r}: not an object")
                continue
            # A field binds widgets either by a top-level widget_id (text /
            # checkbox / radio parent) or by an options map (enum_select /
            # enum_text_select, where each enum value names a widget).
            if not spec.get("widget_id") and not spec.get("options"):
                errors.append(f"field {key!r}: no widget_id or options binding")
            if not spec.get("field_type"):
                errors.append(f"field {key!r}: no field_type")

            conf = spec.get("confidence", "unknown")
            stats[conf] = stats.get(conf, 0) + 1
            if conf == "low":
                reviews.append(f"low confidence: {key}")

            when = spec.get("when")
            if when is not None:
                stats["when_gated"] += 1
                if not _well_formed_when(when):
                    reviews.append(f"unsupported when grammar on {key!r}: {when!r}")

            wid = spec.get("widget_id")
            widget_refs = list(wid if isinstance(wid, list) else ([wid] if wid else []))
            opts = spec.get("options")
            # enum_select / enum_text_select bind widgets through the options map
            # (they carry no widget_id). A radio field carries a widget_id and its
            # options are /AP on-state names, not widgets, so they are not checked.
            if isinstance(opts, dict) and not wid:
                widget_refs.extend(opts.values())
            for w in widget_refs:
                if w is None or inventory is None:
                    continue
                # runtime page-split suffix, incl. same-page duplicates (__p4_1)
                base = re.sub(r"__p\d+(_\d+)?$", "", str(w))
                if base not in inventory and str(w) not in inventory:
                    reviews.append(
                        f"widget not in fields.csv inventory: {key} -> {w!r} "
                        f"(fields.csv may lag a revised blank)"
                    )

            if schema is not None and not _schema_has(
                    schema, spec.get("canonical_key", key)):
                reviews.append(f"key not in schema.json: {key}")

    return {"form_id": form_id, "errors": errors, "reviews": reviews, "stats": stats}


def _print_human(result, verbose):
    fid, st = result["form_id"], result["stats"]
    head = (f"{fid}: {st['fields']} fields "
            f"({st['high']} high / {st['medium']} medium / {st['low']} low, "
            f"{st['when_gated']} conditional)")
    flag = "ERROR" if result["errors"] else ("review" if result["reviews"] else "ok")
    print(f"[{flag}] {head}")
    for e in result["errors"]:
        print(f"    ERROR  {e}")
    if verbose:
        for r in result["reviews"]:
            print(f"    review {r}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("forms", nargs="*", help="form ids (default: all with --all)")
    ap.add_argument("--all", action="store_true", help="validate every form")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="print review findings too")
    args = ap.parse_args(argv)

    targets = args.forms or (
        sorted(d.name for d in FORMS.iterdir() if d.is_dir()) if args.all else [])
    if not targets:
        ap.error("name at least one form id, or pass --all")

    # A single form id is implicitly verbose; a sweep stays terse unless asked.
    verbose = args.verbose or (len(targets) == 1 and not args.all)
    results = [validate_form(f) for f in targets]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            _print_human(r, verbose)
        n_err = sum(len(r["errors"]) for r in results)
        n_rev = sum(len(r["reviews"]) for r in results)
        print(f"\n{len(results)} form(s): {n_err} error(s), {n_rev} review item(s)")

    return 1 if any(r["errors"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
