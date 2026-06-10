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


@pytest.mark.parametrize("fid", FORM_IDS)
def test_schema_property_names_are_addressable(fid):
    """No literal index/placeholder notation in schema property names.

    An earlier generator leaked pass-1 shorthand into literal property names
    ("parties[0]", "class_changes[N]", "line{1,2}", "officer_<role>") —
    unaddressable by engine.canonical dotted paths and shadowing the real
    array/sibling properties. tools/sync_schema.py repairs these; this pins
    the repair.
    """
    import re
    schema = json.loads((FORMS / fid / "schema.json").read_text())
    artifact = re.compile(r"[\[\]{}<>]")
    bad = []

    def walk(node, path):
        for k, v in (node.get("properties") or {}).items():
            if artifact.search(k):
                bad.append(f"{path}{k}")
            if isinstance(v, dict):
                walk(v, f"{path}{k}.")
                if isinstance(v.get("items"), dict):
                    walk(v["items"], f"{path}{k}[].")

    walk(schema, "")
    assert not bad, f"{fid}: artifact property names in schema.json: {bad}"
