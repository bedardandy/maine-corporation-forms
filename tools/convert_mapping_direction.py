#!/usr/bin/env python3
"""Convert every ``forms/*/mapping.json`` to the canonical (field-id-keyed)
direction shared with the sibling forms repos.

The conversion is mechanical, lossless, and idempotent (see
``engine/mapping.py`` for the dialect). Every file is round-trip-verified
before it is written: ``revert(invert(old)) == old`` and
``invert(invert(old)) == invert(old)``; any failure aborts without writing.

    python3 tools/convert_mapping_direction.py            # convert in place
    python3 tools/convert_mapping_direction.py --check    # verify only (CI)
    python3 tools/convert_mapping_direction.py LLC_MLLC-6 # one form

``--check`` exits non-zero if any mapping is still in the legacy direction
or fails the round-trip invariants.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import mapping as mapping_mod  # noqa: E402


def _dump(mapping) -> str:
    return json.dumps(mapping, indent=2, ensure_ascii=False) + "\n"


def convert_file(path: Path, check_only: bool) -> str:
    """Convert one mapping.json. Returns 'converted' | 'ok' | an error string."""
    original = json.loads(path.read_text(encoding="utf-8"))
    if mapping_mod.is_canonical(original):
        # already converted — verify the invariants still hold
        if mapping_mod.invert(original) != original:
            return "ERROR: invert() of a canonical mapping is not a no-op"
        if mapping_mod.invert(mapping_mod.revert(original)) != original:
            return "ERROR: revert/invert round-trip changed the mapping"
        return "ok"
    if check_only:
        return "ERROR: legacy canonical-key-keyed direction"
    converted = mapping_mod.invert(original)
    if mapping_mod.revert(converted) != original:
        return "ERROR: round-trip mismatch (revert(invert(m)) != m); not written"
    if mapping_mod.invert(converted) != converted:
        return "ERROR: invert not idempotent on the converted mapping; not written"
    path.write_text(_dump(converted), encoding="utf-8")
    return "converted"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("forms", nargs="*", help="form ids (default: all)")
    ap.add_argument("--forms-root", default=str(ROOT / "forms"))
    ap.add_argument("--check", action="store_true",
                    help="verify direction + round-trip invariants; write nothing")
    args = ap.parse_args(argv)

    root = Path(args.forms_root)
    targets = args.forms or sorted(
        d.name for d in root.iterdir()
        if d.is_dir() and (d / "mapping.json").exists())

    counts = {"converted": 0, "ok": 0}
    failures = []
    for fid in targets:
        path = root / fid / "mapping.json"
        if not path.exists():
            failures.append(f"{fid}: no mapping.json")
            continue
        try:
            result = convert_file(path, args.check)
        except ValueError as e:
            result = f"ERROR: {e}"
        if result.startswith("ERROR"):
            failures.append(f"{fid}: {result}")
        else:
            counts[result] += 1
            if result == "converted":
                print(f"converted {fid}")

    print(f"\n{counts['converted']} converted, {counts['ok']} already "
          f"canonical, {len(failures)} failure(s)")
    for f in failures:
        print(f"  {f}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
