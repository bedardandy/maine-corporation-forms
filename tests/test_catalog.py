"""Catalog integrity: the indices agree with the form folders on disk."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "forms"

EXPECTED_COUNTS = {  # README scope table, by form-id prefix
    "CORP": 44, "NP": 39, "LLC": 23, "LP": 22, "LLP": 18, "MARK": 7, "GP": 3,
}


def _form_dirs():
    return sorted(d.name for d in FORMS.iterdir() if d.is_dir())


def test_156_form_folders():
    assert len(_form_dirs()) == 156


def test_prefix_counts_match_readme():
    counts = {}
    for fid in _form_dirs():
        counts[fid.split("_")[0]] = counts.get(fid.split("_")[0], 0) + 1
    assert counts == EXPECTED_COUNTS


def test_forms_index_covers_every_folder():
    index = json.loads((ROOT / "catalog" / "forms_index.json").read_text())
    ids = {f["form_id"] for f in index["forms"]}
    assert ids == set(_form_dirs())


def test_by_entity_covers_every_form():
    grouped = json.loads((ROOT / "catalog" / "by_entity.json").read_text())
    listed = {
        fid
        for group in grouped["by_entity_type"].values()
        for fid in group["form_ids"]
    }
    assert listed == set(_form_dirs())


def test_pdf_manifest_is_fetch_on_demand():
    manifest = json.loads((ROOT / "catalog" / "pdf_manifest.json").read_text())["forms"]
    assert set(manifest) == set(_form_dirs())
    # Every blank is fetched on demand; none is redistributed in-repo.
    assert all(p.get("fetch") for p in manifest.values())
    assert all(p.get("url", "").startswith("https://") for p in manifest.values())


def test_no_pdfs_committed():
    # Blank PDFs are fetched on demand to disk; what must never happen is a PDF
    # being *tracked* in git. Check the index, not the working tree.
    import subprocess
    try:
        tracked = subprocess.run(
            ["git", "ls-files", "*.pdf"], cwd=ROOT,
            capture_output=True, text=True, check=True).stdout.split()
    except (FileNotFoundError, subprocess.CalledProcessError):
        import pytest
        pytest.skip("git not available")
    assert tracked == []
