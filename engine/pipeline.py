"""Composable PDF enhancement pipeline.

A small registry of *enhancement steps*, each a thin wrapper over functionality
that already lives in the engine / tools. A caller picks which steps to run (by
id) and the runner threads a shared ``Context`` through them in a fixed,
dependency-respecting order. Adding a capability = one ``STEP`` entry; there are
no per-step modules to keep this from sprawling.

Each step is pure-ish: it reads/writes ``ctx.pdf_bytes`` (and may read
``ctx.case`` / ``ctx.mapping``) and appends a note. Steps that need data they
don't have (e.g. ``fill`` with no case) record a skip rather than raising, so a
partial selection still produces output.

Steps are grouped into tiers the UI can present:

* ``source``        — get the official blank (byte-faithful) or a filled copy
* ``form_fields``   — value/appearance work on the AcroForm
* ``print``         — print-ready output (bake appearances, overflow schedules, flatten)
* ``accessibility`` — PDF-UA-oriented remediation (field /TU, title, lang, tab order)

Nothing here mutates a file on disk except the optional final ``out_path`` write;
the official ``forms/<ID>/<ID>.pdf`` is only ever read.
"""

from __future__ import annotations

import io
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

_ROOT = Path(__file__).resolve().parent.parent


def _forms_root(forms_root: str) -> Path:
    p = Path(forms_root)
    return p if p.is_absolute() else _ROOT / forms_root


# --------------------------------------------------------------------------- #
# Context threaded through the steps
# --------------------------------------------------------------------------- #
@dataclass
class Context:
    form_id: str
    forms_root: str = "forms"
    case: Optional[dict] = None
    pdf_bytes: Optional[bytes] = None
    mapping: Optional[dict] = None
    options: Optional[dict] = None
    notes: list = field(default_factory=list)
    skipped: list = field(default_factory=list)

    def form_dir(self) -> Path:
        return _forms_root(self.forms_root) / self.form_id

    def load_mapping(self) -> dict:
        if self.mapping is None:
            self.mapping = json.loads((self.form_dir() / "mapping.json").read_text())
        return self.mapping

    def form_title(self) -> str:
        try:
            import yaml

            meta = yaml.safe_load((self.form_dir() / "form.yaml").read_text()) or {}
            return meta.get("title") or self.form_id
        except Exception:
            return self.form_id


# --------------------------------------------------------------------------- #
# Step implementations (thin wrappers over existing engine / tools code)
# --------------------------------------------------------------------------- #
def _step_source_blank(ctx: Context) -> None:
    """Load the official blank PDF, byte-faithful from disk."""
    ctx.pdf_bytes = (ctx.form_dir() / f"{ctx.form_id}.pdf").read_bytes()
    ctx.notes.append("loaded official blank PDF")


def _manifest_sha(form_id: str) -> Optional[str]:
    """Return the official SHA-256 for ``form_id`` from catalog/pdf_manifest.json."""
    try:
        man = json.loads((_ROOT / "catalog" / "pdf_manifest.json").read_text())
    except Exception:
        return None
    return (man.get("forms", {}).get(form_id) or {}).get("sha256")


def _step_source_fetch(ctx: Context) -> None:
    """Fetch the official blank from a URL and verify it byte-for-byte.

    The blank is only adopted if its SHA-256 matches ``catalog/pdf_manifest.json``
    for this form — a fetched file is never trusted on filename alone. On any
    failure (no URL, network error, or hash mismatch) the step records a skip and
    leaves the shipped byte-faithful blank in place; a later source step (or the
    implied ``source_blank``) supplies the PDF. The URL is read from
    ``ctx.options['source_url']`` so nothing network-bound is hardcoded.
    """
    import hashlib

    url = (ctx.options or {}).get("source_url") if isinstance(ctx.options, dict) else None
    expected = _manifest_sha(ctx.form_id)
    if not url:
        ctx.skipped.append("source_fetch: no source_url provided; using shipped blank")
        return
    if not expected:
        ctx.skipped.append(
            "source_fetch: no manifest hash to verify against; refusing unverified fetch")
        return
    try:
        import urllib.request

        req = urllib.request.Request(url, headers={"User-Agent": "maine-corp-forms/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (user-supplied URL)
            data = resp.read()
    except Exception as e:
        ctx.skipped.append(f"source_fetch: download failed ({e}); using shipped blank")
        return
    got = hashlib.sha256(data).hexdigest()
    if got != expected:
        ctx.skipped.append(
            f"source_fetch: SHA-256 mismatch (got {got[:12]}…, expected "
            f"{expected[:12]}…); refusing fetched copy, using shipped blank")
        return
    ctx.pdf_bytes = data
    ctx.notes.append(f"fetched official blank from source_url; SHA-256 verified ({got[:12]}…)")


def _step_fill(ctx: Context) -> None:
    """Fill the AcroForm from ``ctx.case`` (deterministic, no LLM)."""
    if not ctx.case:
        ctx.skipped.append("fill: no case data provided")
        return
    from . import fill as _fill

    buf = io.BytesIO()
    _fill.fill_to_stream(ctx.form_id, ctx.case, buf, ctx.forms_root)
    ctx.pdf_bytes = buf.getvalue()
    ctx.notes.append("filled form fields from case data")


def _step_bake_appearances(ctx: Context) -> None:
    """Bake appearance streams so values print in any viewer (no flatten)."""
    from . import printcopy

    if ctx.pdf_bytes is None:
        _step_source_blank(ctx)
    rep = printcopy.make_print_copy(
        ctx.pdf_bytes, ctx.load_mapping(), _tmp_out(ctx, "baked"),
        form_title=ctx.form_title(), entity_name=_entity_name(ctx),
        flatten=False, handle_overflow=False,
    )
    ctx.pdf_bytes = Path(rep["out"]).read_bytes()
    ctx.notes.append("baked appearance streams")


def _step_overflow_schedules(ctx: Context) -> None:
    """Spill over-long values to appended Word-style continuation schedules."""
    from . import printcopy

    if ctx.pdf_bytes is None:
        _step_source_blank(ctx)
    rep = printcopy.make_print_copy(
        ctx.pdf_bytes, ctx.load_mapping(), _tmp_out(ctx, "overflow"),
        form_title=ctx.form_title(), entity_name=_entity_name(ctx),
        flatten=False, handle_overflow=True,
    )
    ctx.pdf_bytes = Path(rep["out"]).read_bytes()
    n = len(rep.get("overflows") or [])
    ctx.notes.append(f"overflow schedules: {n} field(s) spilled")


def _step_print_copy(ctx: Context) -> None:
    """Full print-ready copy: bake + overflow + flatten to static content."""
    from . import printcopy

    if ctx.pdf_bytes is None:
        _step_source_blank(ctx)
    rep = printcopy.make_print_copy(
        ctx.pdf_bytes, ctx.load_mapping(), _tmp_out(ctx, "print"),
        form_title=ctx.form_title(), entity_name=_entity_name(ctx),
        flatten=True, handle_overflow=True,
    )
    ctx.pdf_bytes = Path(rep["out"]).read_bytes()
    ctx.notes.append("flattened print-ready copy")


def _step_accessibility(ctx: Context) -> None:
    """PDF-UA-oriented remediation: field /TU tooltips, title, language."""
    try:
        import pypdf

        from tools.accessibility import remediate_form
    except Exception as e:  # pragma: no cover
        ctx.skipped.append(f"accessibility: unavailable ({e})")
        return
    if ctx.pdf_bytes is None:
        _step_source_blank(ctx)
    reader = pypdf.PdfReader(io.BytesIO(ctx.pdf_bytes))
    result = remediate_form.remediate(
        reader, ctx.load_mapping(), title=ctx.form_title(), lang="en-US"
    )
    # remediate() returns (writer, report); tolerate a bare writer too.
    writer, report = result if isinstance(result, tuple) else (result, {})
    buf = io.BytesIO()
    writer.write(buf)
    ctx.pdf_bytes = buf.getvalue()
    tu = report.get("tooltips_set") if isinstance(report, dict) else None
    ctx.notes.append(
        f"accessibility: /TU tooltips ({tu}), title, lang set" if tu is not None
        else "accessibility: /TU tooltips, title, lang set"
    )


def _entity_name(ctx: Context) -> str:
    ent = (ctx.case or {}).get("entity") if isinstance(ctx.case, dict) else None
    return str(ent.get("name") or "") if isinstance(ent, dict) else ""


def _tmp_out(ctx: Context, tag: str) -> str:
    import tempfile

    fd, path = tempfile.mkstemp(prefix=f"{ctx.form_id}_{tag}_", suffix=".pdf")
    import os

    os.close(fd)
    return path


# --------------------------------------------------------------------------- #
# Registry — one entry per enhancement. order = pipeline execution order.
# --------------------------------------------------------------------------- #
@dataclass
class Step:
    id: str
    label: str
    tier: str
    description: str
    run: Callable[[Context], None]
    order: int
    needs_case: bool = False


STEPS = [
    Step("source_blank", "Official blank form", "source",
         "Load the byte-faithful blank PDF as filed by the Secretary of State.",
         _step_source_blank, order=10),
    Step("source_fetch", "Download official copy (verified)", "source",
         "Download the blank from a source URL and adopt it only if its SHA-256 "
         "matches the recorded official hash; otherwise keep the shipped blank.",
         _step_source_fetch, order=11),
    Step("fill", "Fill from case data", "form_fields",
         "Populate the AcroForm fields from a structured case object (deterministic).",
         _step_fill, order=20, needs_case=True),
    Step("bake_appearances", "Bake appearances (print-faithful)", "print",
         "Regenerate appearance streams so filled values print in any viewer.",
         _step_bake_appearances, order=30),
    Step("overflow_schedules", "Overflow → continuation schedules", "print",
         "Spill over-long answers onto appended Word-style schedule pages.",
         _step_overflow_schedules, order=40),
    Step("print_copy", "Flatten print-ready copy", "print",
         "Bake + overflow + flatten to static content (cannot be re-edited).",
         _step_print_copy, order=50),
    Step("accessibility", "Accessibility remediation (PDF-UA)", "accessibility",
         "Add field tooltips (/TU), document title, and language for screen readers.",
         _step_accessibility, order=60),
]
_BY_ID = {s.id: s for s in STEPS}


def list_steps() -> list:
    """Registry as plain dicts (for the API / UI)."""
    return [
        {"id": s.id, "label": s.label, "tier": s.tier,
         "description": s.description, "needs_case": s.needs_case, "order": s.order}
        for s in sorted(STEPS, key=lambda s: s.order)
    ]


def run_pipeline(form_id: str, step_ids, case: dict = None, *,
                 forms_root: str = "forms", out_path: str = None,
                 options: dict = None) -> dict:
    """Run the selected steps in registry order; return bytes + a run report.

    Unknown step ids are reported, not fatal. ``source_blank`` is implied if no
    source step is selected, so a fill/print/accessibility selection still has a
    PDF to operate on. ``options`` carries non-case parameters such as
    ``source_url`` for the ``source_fetch`` step.
    """
    ids = list(step_ids or [])
    unknown = [i for i in ids if i not in _BY_ID]
    chosen = [_BY_ID[i] for i in ids if i in _BY_ID]
    chosen.sort(key=lambda s: s.order)
    if not any(s.tier == "source" for s in chosen):
        chosen.insert(0, _BY_ID["source_blank"])
    elif _BY_ID["source_fetch"] in chosen and _BY_ID["source_blank"] not in chosen:
        # source_fetch may decline (no URL / hash mismatch); ensure a blank backs it.
        chosen.insert(0, _BY_ID["source_blank"])

    ctx = Context(form_id=form_id, forms_root=forms_root, case=case, options=options)
    ran = []
    for s in chosen:
        s.run(ctx)
        ran.append(s.id)

    if out_path and ctx.pdf_bytes is not None:
        Path(out_path).write_bytes(ctx.pdf_bytes)

    return {
        "form_id": form_id,
        "ran": ran,
        "unknown_steps": unknown,
        "notes": ctx.notes,
        "skipped": ctx.skipped,
        "bytes": ctx.pdf_bytes,
        "size": len(ctx.pdf_bytes) if ctx.pdf_bytes else 0,
    }


def _main(argv) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Run the PDF enhancement pipeline")
    ap.add_argument("form_id")
    ap.add_argument("--steps", default="", help="comma list of step ids")
    ap.add_argument("--case", help="path to case JSON")
    ap.add_argument("--out")
    ap.add_argument("--source-url", help="URL for the source_fetch step (verified by hash)")
    ap.add_argument("--list", action="store_true", help="list steps and exit")
    a = ap.parse_args(argv)
    if a.list:
        print(json.dumps(list_steps(), indent=2))
        return 0
    if not a.out:
        ap.error("--out is required unless --list")
    case = json.loads(Path(a.case).read_text()) if a.case else None
    ids = [s.strip() for s in a.steps.split(",") if s.strip()]
    options = {"source_url": a.source_url} if a.source_url else None
    rep = run_pipeline(a.form_id, ids, case, out_path=a.out, options=options)
    rep.pop("bytes", None)
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(_main(sys.argv[1:]))
