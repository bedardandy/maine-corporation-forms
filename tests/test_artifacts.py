"""Every form folder carries the full, parseable artifact set."""
import csv
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "forms"
FORM_IDS = sorted(d.name for d in FORMS.iterdir() if d.is_dir())

REQUIRED = ["form.yaml", "mapping.json", "schema.json", "fields.csv",
            "rubric.yaml", "README.md", "SKILL.md"]


@pytest.mark.parametrize("fid", FORM_IDS)
def test_required_files_present(fid):
    for name in REQUIRED:
        assert (FORMS / fid / name).exists(), f"{fid} missing {name}"


@pytest.mark.parametrize("fid", FORM_IDS)
def test_json_and_yaml_parse(fid):
    d = FORMS / fid
    json.loads((d / "mapping.json").read_text())
    json.loads((d / "schema.json").read_text())
    yaml.safe_load((d / "form.yaml").read_text())
    yaml.safe_load((d / "rubric.yaml").read_text())
    with open(d / "fields.csv", newline="") as f:
        reader = csv.DictReader(f)
        list(reader)  # a flat/reference doc may legitimately have zero rows
    assert reader.fieldnames and "widget_id" in reader.fieldnames, \
        f"{fid} fields.csv missing header"


@pytest.mark.parametrize("fid", FORM_IDS)
def test_mapping_form_id_matches_folder(fid):
    mapping = json.loads((FORMS / fid / "mapping.json").read_text())
    assert mapping["form_id"] == fid
