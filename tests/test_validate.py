"""The per-form validator finds zero structural errors across the library.

Review-level findings (fields.csv inventory lag, schema backlog, low
confidence) are allowed — they are the documented modular-improvement worklist,
not failures. Structural errors (unparseable files, a field that binds no
widget) are not allowed.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import validate_form  # noqa: E402

FORM_IDS = sorted(d.name for d in (ROOT / "forms").iterdir() if d.is_dir())


def test_zero_structural_errors():
    offenders = {}
    for fid in FORM_IDS:
        errors = validate_form.validate_form(fid)["errors"]
        if errors:
            offenders[fid] = errors
    assert not offenders, f"forms with structural errors: {offenders}"


def test_empty_forms_are_non_acroform():
    # A form may have zero mapped fields only if it carries no AcroForm (a flat
    # reference document). An AcroForm form with zero fields is an unmapped gap.
    import json
    manifest = json.loads(
        (ROOT / "catalog" / "pdf_manifest.json").read_text())["forms"]
    for fid in FORM_IDS:
        if validate_form.validate_form(fid)["stats"]["fields"] == 0:
            assert manifest[fid].get("has_acroform") is False, \
                f"{fid} has an AcroForm but no mapped fields"
