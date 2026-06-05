#!/usr/bin/env python3
"""CLI: export one or all Maine SoS forms to a templating-system target.

    python3 tools/export/export_form.py --form CORP_MBCA-6 --target esign
    python3 tools/export/export_form.py --all --target interchange --out build/
    python3 tools/export/export_form.py --form CORP_MBCA-6 --target all --out build/

Targets: interchange | esign | docassembly | gavel | all

Writes each artifact under ``<out>/<form_id>/<target>/``. With no ``--out`` the
files print to stdout (single form + single target only).
"""
from __future__ import annotations

import argparse
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve()
_REPO_ROOT = _HERE.parent.parent.parent
sys.path.insert(0, str(_HERE.parent.parent))  # so `export` is importable

from export.model import build_model  # noqa: E402
from export.exporters import EXPORTERS  # noqa: E402


def _all_form_ids(repo_root):
    root = repo_root / "forms"
    return sorted(p.name for p in root.iterdir()
                  if p.is_dir() and (p / "mapping.json").exists())


def export_one(form_id, target, repo_root):
    model = build_model(form_id, repo_root)
    if target == "all":
        out = {}
        for name, fn in EXPORTERS.items():
            for fname, content in fn(model).items():
                out[f"{name}/{fname}"] = content
        return out
    if target not in EXPORTERS:
        raise SystemExit(f"unknown target {target!r} "
                         f"(choices: {', '.join(EXPORTERS)}, all)")
    return EXPORTERS[target](model)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--form", help="form_id to export")
    g.add_argument("--all", action="store_true", help="export all forms")
    ap.add_argument("--target", required=True,
                    help="interchange | esign | docassembly | gavel | all")
    ap.add_argument("--out", type=pathlib.Path,
                    help="output dir (required for --all or --target all)")
    a = ap.parse_args()

    repo_root = _REPO_ROOT
    form_ids = _all_form_ids(repo_root) if a.all else [a.form]

    if not a.out:
        if a.all or a.target == "all":
            raise SystemExit("--out is required for --all or --target all")
        for fname, content in export_one(form_ids[0], a.target, repo_root).items():
            print(f"===== {fname} =====")
            print(content)
        return 0

    for form_id in form_ids:
        out = export_one(form_id, a.target, repo_root)
        base = a.out / form_id
        for fname, content in out.items():
            path = base / fname
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
