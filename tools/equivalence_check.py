#!/usr/bin/env python3
"""Fill-engine equivalence harness: old pypdf path vs. shared PyMuPDF core.

For every form, fills a deterministic synthetic case through BOTH engines and
asserts the resulting AcroForm field values are semantically equal:

- the **old** path: this repo's pre-migration pypdf filler, materialized from
  git history (:data:`BASELINE_SHA`, the last commit before the
  ``maine-forms-engine`` fill-core migration) into a temporary worktree, fed
  its own legacy-direction ``mapping.json`` from that same commit;
- the **new** path: the working tree's ``engine.fill`` (shared
  ``maine_forms_engine`` PyMuPDF core + repo policy), fed the converted
  canonical-direction ``mapping.json``.

Byte-identity across pypdf/PyMuPDF is impossible (different writers; PyMuPDF
also regenerates the trailer ``/ID``), so equality is per-field **semantic**:
text values must match exactly; button fields must agree on their on-state
(``/Off`` and "no ``/V`` at all" both mean unchecked).

The synthetic case sets every mapped canonical key once: enum/radio bindings
get their first declared option, checkboxes ``true``, text a deterministic
placeholder. ``when``-gated branches evaluate identically in both engines by
construction, so whichever branch the case activates is compared faithfully.
Preflight and the blank-revision guard are off — this compares *fill engines*,
not case validity.

    python3 tools/equivalence_check.py                # all forms
    python3 tools/equivalence_check.py LLC_MLLC-6 ... # subset
    python3 tools/equivalence_check.py --json out.json

Exits non-zero when any form diverges; the report lists every differing field
with both values.

Known, intentional divergences (verified 2026-06-11, 154/156 identical):

- ``NP_MNPCA-6`` ``cra`` and ``LLC_MLLC-12`` ``Check Box15``/``16`` — on both
  forms ``registered_agent.type`` is a *text*-typed binding fanned onto
  checkbox widgets. The old pypdf filler wrote the literal type string into
  the button ``/V`` — an invalid state no viewer renders (the box stays
  unchecked) but corrupted value data. The shared core refuses the
  radio-encoded pair (``cra``, soft-locked with a yellow-light report entry)
  and normalizes the plain checkboxes to a clean explicit ``/Off``; rendered
  output is identical, the stored values are now valid. Re-binding
  ``registered_agent.type`` as enum options on these two forms is mapping
  enrichment, tracked separately from the engine migration.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.mapping import entries as mapping_entries  # noqa: E402

#: Last commit whose engine/fill.py is the pypdf reference filler (and whose
#: mapping.json files are in the legacy canonical-key-keyed direction).
BASELINE_SHA = "9095881"

# Driver executed inside each tree (old worktree / current repo) so each
# engine runs against its own code + mapping dialect. Reads a job file
# {jobs: [{form_id, case, forms_root, out_pdf}]}, fills with preflight and
# blank verification off, writes one status line per job.
_DRIVER = r"""
import json, sys, traceback
from engine import fill

jobs = json.loads(open(sys.argv[1], encoding="utf-8").read())["jobs"]
results = []
for j in jobs:
    try:
        fill.fill(j["form_id"], j["case"], j["out_pdf"], j["forms_root"],
                  verify_blank="off", preflight="off")
        results.append({"form_id": j["form_id"], "ok": True})
    except Exception as e:
        results.append({"form_id": j["form_id"], "ok": False,
                        "error": f"{type(e).__name__}: {e}",
                        "trace": traceback.format_exc()})
print(json.dumps(results))
"""


# --------------------------------------------------------------------------
# deterministic synthetic case from a form's mapping
# --------------------------------------------------------------------------
def _set_dotted(case, dotted, value):
    """Set ``a.b[0].c`` into nested dicts/lists; first writer wins."""
    parts = dotted.replace("]", "").replace("[", ".").split(".")
    cur = case
    for i, part in enumerate(parts):
        last = i == len(parts) - 1
        nxt_is_index = not last and parts[i + 1].isdigit()
        if part.isdigit():
            idx = int(part)
            while len(cur) <= idx:
                cur.append([] if nxt_is_index else {})
            if last:
                return  # a bare list index can't be a leaf here
            cur = cur[idx]
        else:
            if last:
                if part not in cur:
                    cur[part] = value
                return
            if part not in cur or not isinstance(cur[part], (dict, list)):
                if part in cur:
                    return  # a scalar already sits on this path; keep it
                cur[part] = [] if nxt_is_index else {}
            cur = cur[part]


def build_case(mapping) -> dict:
    """One deterministic value per mapped canonical key (see module doc)."""
    case: dict = {}
    for n, (key, spec) in enumerate(mapping_entries(mapping).items()):
        ckey = spec.get("canonical_key", key)
        ft = spec.get("field_type", "text")
        if ft in ("radio", "enum_select", "enum_text_select"):
            options = spec.get("options") or {}
            if not options:
                continue
            value = next(iter(options))
            # JSON-boolean-alias enums ("True"/"true"/"yes") stay strings —
            # both engines stringify identically either way.
        elif ft in ("checkbox", "boolean"):
            value = True
        else:
            leaf = ckey.rsplit(".", 1)[-1]
            value = f"EQV {n:03d} {leaf}"[:60]
        _set_dotted(case, ckey, value)
    return case


# --------------------------------------------------------------------------
# field-value extraction + normalization
# --------------------------------------------------------------------------
def button_names(pdf_path) -> set:
    """Field names typed ``/Btn`` in a PDF (read from the blank, so both
    engines' outputs are classified identically — the writers differ in how
    faithfully they carry ``/FT`` on orphan fields)."""
    import pypdf

    reader = pypdf.PdfReader(str(pdf_path))
    return {name for name, f in (reader.get_fields() or {}).items()
            if str(f.get("/FT") or "") == "/Btn"}


def extract_values(pdf_path, blank_buttons: set) -> dict:
    """``{field_name: normalized /V}`` for every AcroForm field.

    Buttons normalize ``None`` / ``""`` / ``/Off`` to ``"Off"`` (all mean
    unchecked); other fields normalize ``None`` to ``""``. Button-ness comes
    from the blank when the name exists there, else from the output itself
    (runtime-split promoted names exist only in the outputs)."""
    import pypdf

    reader = pypdf.PdfReader(str(pdf_path))
    fields = reader.get_fields() or {}
    out = {}
    for name, f in fields.items():
        v = f.get("/V")
        is_btn = (name in blank_buttons
                  or str(f.get("/FT") or "") == "/Btn")
        if is_btn:
            s = "" if v is None else str(v)
            s = s.lstrip("/")
            out[name] = "Off" if s in ("", "Off") else s
        else:
            out[name] = "" if v is None else str(v)
    return out


def compare(old_vals, new_vals, blank_buttons: set) -> list:
    """Per-field diffs. A field absent from one output was never written:
    that is "Off" for a button and "" for a text field (pypdf drops orphan
    fields entirely on rewrite; PyMuPDF carries them)."""
    diffs = []
    for name in sorted(set(old_vals) | set(new_vals)):
        default = "Off" if name in blank_buttons else ""
        ov = old_vals.get(name, default)
        nv = new_vals.get(name, default)
        if ov != nv:
            diffs.append({"field": name, "old": ov, "new": nv})
    return diffs


# --------------------------------------------------------------------------
# the two engine runs
# --------------------------------------------------------------------------
def _run_driver(tree: Path, job_path: Path) -> dict:
    proc = subprocess.run(
        [sys.executable, "-c", _DRIVER, str(job_path)],
        cwd=tree, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"driver failed in {tree}:\n{proc.stderr[-2000:]}")
    return {r["form_id"]: r for r in json.loads(proc.stdout)}


def _materialize_baseline(workdir: Path) -> Path:
    """Detached worktree of :data:`BASELINE_SHA` (old code + old mappings)."""
    tree = workdir / "baseline"
    subprocess.run(["git", "-C", str(ROOT), "worktree", "add", "--detach",
                    str(tree), BASELINE_SHA],
                   check=True, capture_output=True)
    return tree


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("forms", nargs="*", help="form ids (default: all)")
    ap.add_argument("--json", type=Path, help="write the full report here")
    args = ap.parse_args(argv)

    form_ids = args.forms or sorted(
        d.name for d in (ROOT / "forms").iterdir()
        if d.is_dir() and (d / "mapping.json").exists())

    report = {"baseline": BASELINE_SHA, "forms": {}}
    identical = diverged = errored = 0

    with tempfile.TemporaryDirectory(prefix="mcorp_eqv_") as td:
        work = Path(td)
        baseline = _materialize_baseline(work)
        try:
            # The baseline worktree has no blank PDFs (they are fetched, not
            # tracked); both engines must fill the SAME blank bytes anyway, so
            # each baseline form dir gets the legacy mapping from git plus a
            # symlink to the working tree's pinned blank.
            old_root = work / "old_forms"
            old_jobs, new_jobs = [], []
            skipped = []
            for fid in form_ids:
                blank = ROOT / "forms" / fid / f"{fid}.pdf"
                legacy_mapping = baseline / "forms" / fid / "mapping.json"
                if not blank.exists() or not legacy_mapping.exists():
                    skipped.append(fid)
                    report["forms"][fid] = {
                        "status": "skipped",
                        "reason": ("blank not on disk" if not blank.exists()
                                   else "form not in baseline commit")}
                    continue
                mapping = json.loads(
                    (ROOT / "forms" / fid / "mapping.json").read_text())
                case = build_case(mapping)
                d = old_root / fid
                d.mkdir(parents=True)
                (d / "mapping.json").write_text(legacy_mapping.read_text())
                (d / f"{fid}.pdf").symlink_to(blank)
                old_jobs.append({"form_id": fid, "case": case,
                                 "forms_root": str(old_root),
                                 "out_pdf": str(work / f"{fid}.old.pdf")})
                new_jobs.append({"form_id": fid, "case": case,
                                 "forms_root": str(ROOT / "forms"),
                                 "out_pdf": str(work / f"{fid}.new.pdf")})

            (work / "old_jobs.json").write_text(json.dumps({"jobs": old_jobs}))
            (work / "new_jobs.json").write_text(json.dumps({"jobs": new_jobs}))
            old_res = _run_driver(baseline, work / "old_jobs.json")
            new_res = _run_driver(ROOT, work / "new_jobs.json")

            for job in old_jobs:
                fid = job["form_id"]
                o, n = old_res[fid], new_res[fid]
                if not o["ok"] or not n["ok"]:
                    errored += 1
                    report["forms"][fid] = {
                        "status": "error",
                        "old_error": o.get("error"),
                        "new_error": n.get("error")}
                    continue
                blank_btns = button_names(ROOT / "forms" / fid / f"{fid}.pdf")
                diffs = compare(
                    extract_values(work / f"{fid}.old.pdf", blank_btns),
                    extract_values(work / f"{fid}.new.pdf", blank_btns),
                    blank_btns)
                if diffs:
                    diverged += 1
                    report["forms"][fid] = {"status": "diverged",
                                            "diffs": diffs}
                else:
                    identical += 1
                    report["forms"][fid] = {"status": "identical"}
        finally:
            subprocess.run(["git", "-C", str(ROOT), "worktree", "remove",
                            "--force", str(baseline)], capture_output=True)

    total = identical + diverged + errored
    print(f"equivalence: {identical}/{total} identical, {diverged} diverged, "
          f"{errored} errored"
          + (f", {len(skipped)} skipped ({', '.join(skipped)})" if skipped
             else ""))
    for fid, r in report["forms"].items():
        if r["status"] == "diverged":
            print(f"\n  {fid}:")
            for d in r["diffs"]:
                print(f"    {d['field']!r}: old={d['old']!r} new={d['new']!r}")
        elif r["status"] == "error":
            print(f"\n  {fid}: old_error={r.get('old_error')!r} "
                  f"new_error={r.get('new_error')!r}")
    if args.json:
        args.json.write_text(json.dumps(report, indent=2))
        print(f"\nfull report: {args.json}")
    return 1 if (diverged or errored) else 0


if __name__ == "__main__":
    sys.exit(main())
