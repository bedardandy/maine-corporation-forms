#!/usr/bin/env python3
"""Validate every SKILL.md embedded example against its form's schema.json.

Each ``forms/<ID>/SKILL.md`` carries an "Example case data" JSON block that
agents copy as a starting point — so it must satisfy the form's own schema.
This extracts each block and runs :func:`engine.schema.validate` over it.

Exit code is non-zero if any example fails, so it gates CI (the same check
runs in the test suite; this CLI gives the full per-form detail).

    python3 tools/lint_skill_examples.py            # all forms
    python3 tools/lint_skill_examples.py LLC_MLLC-6 # one form
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import schema as eschema  # noqa: E402

_EXAMPLE_RE = re.compile(r"## Example case data\n\n```json\n(.*?)```", re.S)
_ARTIFACT_KEY_RE = re.compile(r"[\[\]{}<>]")


def artifact_keys(obj, path=""):
    """Dict keys carrying index/placeholder notation (``"entities[0]"``).

    Such literal keys are a generator artifact: ``engine.canonical`` resolves
    ``entities[0].name`` as array indexing, so a literal ``"entities[0]"``
    key silently fills nothing. Examples must use real JSON arrays.
    """
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if _ARTIFACT_KEY_RE.search(str(k)):
                found.append(f"{path}{k}")
            found.extend(artifact_keys(v, f"{path}{k}."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found.extend(artifact_keys(v, f"{path}[{i}]."))
    return found



def extract_example(skill_text: str):
    """Return the embedded example dict, or ``None`` if there is no block.

    Raises ``json.JSONDecodeError`` when a block exists but does not parse.
    """
    m = _EXAMPLE_RE.search(skill_text)
    if not m:
        return None
    return json.loads(m.group(1))


def lint(form_ids=None, forms_root=None) -> dict:
    """Return ``{form_id: [error, ...]}`` for every failing example."""
    root = pathlib.Path(forms_root) if forms_root else ROOT / "forms"
    failures = {}
    for d in sorted(root.iterdir()):
        if not d.is_dir() or (form_ids and d.name not in form_ids):
            continue
        sk = d / "SKILL.md"
        if not sk.exists() or not (d / "schema.json").exists():
            continue
        try:
            case = extract_example(sk.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            failures[d.name] = [f"example block is not valid JSON: {e}"]
            continue
        if case is None:
            continue
        errors = eschema.validate(d.name, case, str(root))
        errors.extend(
            f"{k}: literal bracketed/braced key — use a real JSON array "
            "(generator artifact; fills nothing)"
            for k in artifact_keys(case))
        if errors:
            failures[d.name] = errors
    return failures


def main(argv) -> int:
    failures = lint(set(argv[1:]) or None)
    for fid, errors in failures.items():
        for e in errors:
            print(f"  {fid}: {e}")
    print(f"\n{len(failures)} form(s) with an invalid SKILL.md example")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
