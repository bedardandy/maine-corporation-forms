"""Every SKILL.md embedded example must satisfy its own form's schema.json.

Agents copy these blocks as fill starting points; an example the form's own
schema rejects teaches the wrong shape. tools/lint_skill_examples.py gives the
per-form CLI detail.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import lint_skill_examples  # noqa: E402


def test_every_embedded_example_validates():
    failures = lint_skill_examples.lint()
    pretty = "\n".join(f"{fid}: {errs}" for fid, errs in failures.items())
    assert not failures, f"invalid SKILL.md examples:\n{pretty}"
