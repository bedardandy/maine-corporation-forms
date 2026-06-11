"""``built_against_sha256`` stamps must match the manifest-pinned blanks.

The stamp is the staleness gate of the MRS-1041ME incident class: a mapping
that says fillable while the manifest (and the re-fetched blank) moved on.
``tools/verify_mapping_fields.py`` writes it only after an honest
re-verification, so any stamp/manifest disagreement here means either the
manifest was re-pinned without re-verifying the mapping, or the stamp was
back-filled by hand — both must fail loudly.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "forms"
MANIFEST = ROOT / "catalog" / "pdf_manifest.json"


def _mappings():
    for d in sorted(FORMS.iterdir()):
        mp = d / "mapping.json"
        if d.is_dir() and mp.exists():
            yield d.name, json.loads(mp.read_text(encoding="utf-8"))


def test_every_stamp_matches_the_manifest():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["forms"]
    mismatches = []
    stamped = 0
    for fid, mapping in _mappings():
        sha = mapping.get("built_against_sha256")
        if not sha:
            continue
        stamped += 1
        pinned = (manifest.get(fid) or {}).get("sha256")
        if sha != pinned:
            mismatches.append(f"{fid}: stamped {sha} != manifest {pinned}")
    assert not mismatches, (
        "stale built_against_sha256 stamp(s) — re-verify with "
        "tools/verify_mapping_fields.py, re-map if widgets moved:\n"
        + "\n".join(mismatches))
    assert stamped, "no stamped mappings found — the gate is vacuous"


def test_every_mapped_form_is_stamped():
    # Every form with a non-empty map carries the stamp; only reference
    # documents with an intentionally empty map (MARK_mark5, see
    # docs/upstream-worklist.md) verify nothing and stay unstamped.
    unstamped = [fid for fid, mapping in _mappings()
                 if mapping.get("map") and "built_against_sha256" not in mapping]
    assert not unstamped, (
        "mapped form(s) without built_against_sha256 — run "
        f"tools/verify_mapping_fields.py --stamp after verifying: {unstamped}")
