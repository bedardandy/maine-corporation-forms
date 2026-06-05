"""Orchestrate the Qwen+Opus audit loop over one or many forms.

Pipeline per case (deterministic stages first, Opus last):

  factgen -> coverage gate -> signer-rule validation -> fill+render -> Opus
  visual pass + Opus logic pass -> per-case verdict.

Endpoints come from the environment (see ``tools/audit/llm.py``). With
``AUDIT_OFFLINE=1`` the Opus passes are skipped but every deterministic stage and
the render still run, so the plumbing is verifiable without network access.

Usage:
  python3 -m tools.audit.run --form CORP_MBCA-6 [--qwen] [--seed 1] [--out DIR]
  python3 -m tools.audit.run --all [--limit 10]
  python3 -m tools.audit.run --form CORP_MBCA-6 --variants typical,overflow
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import audit, factgen, render
from .. import signer_rules


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _all_form_ids():
    forms = _repo_root() / "forms"
    return sorted(
        d.name for d in forms.iterdir() if d.is_dir() and (d / "form.yaml").exists()
    )


def _plan(form_id: str, case: dict) -> dict:
    """Build the coverage plan once; return both the summary and resolved values."""
    try:
        from engine import plan

        p = plan.build_plan(form_id, case)
        cov = p.get("coverage", {})
        return {
            "coverage": {
                "resolved": cov.get("resolved"),
                "unresolved_required": cov.get("unresolved_required"),
                "skipped": cov.get("skipped"),
                "ok": (cov.get("unresolved_required", 0) == 0),
            },
            "resolved_values": p.get("resolved") or {},
        }
    except Exception as e:
        return {"coverage": {"error": str(e), "ok": None}, "resolved_values": {}}


def _rubric_checks(form_id: str):
    fd = _repo_root() / "forms" / form_id
    try:
        import yaml

        data = yaml.safe_load((fd / "rubric.yaml").read_text()) or {}
        checks = data.get("checks") or data.get("rubric") or []
        out = []
        for c in checks if isinstance(checks, list) else []:
            if isinstance(c, dict):
                out.append(
                    {
                        "id": c.get("id"),
                        "severity": c.get("severity"),
                        "desc": (c.get("description") or c.get("desc") or "")[:200],
                    }
                )
        return out[:40]
    except Exception:
        return []


def _form_title(form_id: str) -> str:
    fd = _repo_root() / "forms" / form_id
    try:
        import yaml

        return (yaml.safe_load((fd / "form.yaml").read_text()) or {}).get(
            "title", form_id
        )
    except Exception:
        return form_id


def run_case(form_id: str, variant: str, case: dict, out_dir: str) -> dict:
    rules = signer_rules.rules_for(form_id)
    planned = _plan(form_id, case)
    cov = planned["coverage"]
    signer_issues = signer_rules.validate(form_id, case)

    case_dir = Path(out_dir) / form_id / variant
    rendered = render.render_case(form_id, case, str(case_dir))
    # The print copy is flattened (no widgets), so read placed values from the
    # plan's resolved map rather than the flattened PDF.
    values = planned["resolved_values"]

    visual = audit.visual_pass(form_id, rendered["pages"])
    logic = audit.logic_pass(
        form_id,
        title=_form_title(form_id),
        values=values,
        rules=rules,
        rubric_checks=_rubric_checks(form_id),
    )

    expect_signer_fail = variant == "signer_bad"
    signer_failed = any(i["severity"] == "required" for i in signer_issues)
    signer_gate_ok = signer_failed == expect_signer_fail

    expect_overflow = variant == "overflow"
    got_overflow = len(rendered["overflows"]) > 0

    return {
        "form_id": form_id,
        "variant": variant,
        "coverage": cov,
        "signer_issues": signer_issues,
        "signer_gate_ok": signer_gate_ok,
        "overflows": rendered["overflows"],
        "overflow_expectation_ok": (got_overflow if expect_overflow else True),
        "pages": rendered["pages"],
        "visual": visual,
        "logic": logic,
    }


def run_form(form_id: str, *, seed: int, use_qwen: bool, out_dir: str, variants=None,
             done=None, on_result=None) -> list:
    cases = factgen.generate(form_id, seed=seed, use_qwen=use_qwen)
    if variants:
        cases = {k: v for k, v in cases.items() if k in variants}
    done = done or set()
    results = []
    for name, case in cases.items():
        if (form_id, name) in done:
            continue
        try:
            r = run_case(form_id, name, case, out_dir)
        except Exception as e:
            r = {"form_id": form_id, "variant": name, "fatal": str(e)}
        results.append(r)
        if on_result is not None:
            on_result(r)
    return results


def _load_checkpoint(path: Path) -> list:
    """Read previously completed case records from a JSONL checkpoint."""
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def _summary_row(r: dict) -> str:
    cov = r.get("coverage", {})
    vis = r.get("visual", {})
    log = r.get("logic", {})
    return "\t".join(
        str(x)
        for x in [
            r.get("form_id"),
            r.get("variant"),
            cov.get("resolved"),
            cov.get("unresolved_required"),
            "signer_ok" if r.get("signer_gate_ok") else "SIGNER_FAIL",
            len(r.get("overflows", [])),
            vis.get("status", "-"),
            (vis.get("reads_correctly") if vis.get("status") == "ok" else "-"),
            log.get("status", "-"),
            (log.get("coherent") if log.get("status") == "ok" else "-"),
            r.get("fatal", ""),
        ]
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Qwen+Opus audit loop")
    ap.add_argument("--form", help="single form id")
    ap.add_argument("--forms", default="", help="comma list of form ids (a subset)")
    ap.add_argument("--all", action="store_true", help="run every form")
    ap.add_argument("--limit", type=int, default=0, help="cap --all count")
    ap.add_argument("--qwen", action="store_true", help="enrich via Qwen")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--variants", default="", help="comma list to restrict")
    ap.add_argument("--out", default=str(_repo_root() / "build" / "audit"))
    ap.add_argument("--resume", action="store_true",
                    help="skip cases already in the checkpoint JSONL")
    args = ap.parse_args(argv)

    if args.all:
        form_ids = _all_form_ids()
        if args.limit:
            form_ids = form_ids[: args.limit]
    elif args.forms:
        form_ids = [f.strip() for f in args.forms.split(",") if f.strip()]
    elif args.form:
        form_ids = [args.form]
    else:
        ap.error("specify --form ID, --forms A,B,C, or --all")
        return 2

    variants = [v.strip() for v in args.variants.split(",") if v.strip()] or None

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    ckpt = out / "checkpoint.jsonl"

    prior = _load_checkpoint(ckpt) if args.resume else []
    done = {(r.get("form_id"), r.get("variant")) for r in prior}
    all_results = list(prior)
    if done:
        print(f"resuming: {len(done)} cases already done", flush=True)

    ckpt_fh = open(ckpt, "a" if args.resume else "w", encoding="utf-8")

    def _checkpoint(r: dict) -> None:
        ckpt_fh.write(json.dumps(r) + "\n")
        ckpt_fh.flush()

    for i, fid in enumerate(form_ids, 1):
        res = run_form(
            fid,
            seed=args.seed,
            use_qwen=args.qwen,
            out_dir=args.out,
            variants=variants,
            done=done,
            on_result=_checkpoint,
        )
        all_results.extend(res)
        print(f"[{i}/{len(form_ids)}] {fid}: +{len(res)} cases "
              f"(total {len(all_results)})", flush=True)

    ckpt_fh.close()
    (out / "report.json").write_text(json.dumps(all_results, indent=2))
    header = (
        "form\tvariant\tresolved\tunresolved_req\tsigner\toverflows\t"
        "visual\treads_ok\tlogic\tcoherent\tfatal"
    )
    rows = [header] + [_summary_row(r) for r in all_results]
    (out / "summary.tsv").write_text("\n".join(rows) + "\n")

    n = len(all_results)
    signer_fail = sum(1 for r in all_results if not r.get("signer_gate_ok"))
    fatals = sum(1 for r in all_results if r.get("fatal"))
    print(
        json.dumps(
            {
                "cases": n,
                "signer_gate_failures": signer_fail,
                "fatals": fatals,
                "report": str(out / "report.json"),
                "summary": str(out / "summary.tsv"),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
