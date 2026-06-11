"""Every mapping.json is in the canonical (field-id-keyed) direction and the
direction converter is lossless + idempotent on it (engine/mapping.py)."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import mapping as mapping_mod  # noqa: E402

FORMS = ROOT / "forms"
FORM_IDS = sorted(d.name for d in FORMS.iterdir() if d.is_dir())


@pytest.mark.parametrize("fid", FORM_IDS)
def test_mapping_is_canonical_direction_and_round_trips(fid):
    mapping = json.loads((FORMS / fid / "mapping.json").read_text())
    assert mapping_mod.is_canonical(mapping), \
        f"{fid}: legacy canonical-key-keyed mapping.json — run " \
        "tools/convert_mapping_direction.py"
    # idempotent: inverting a canonical mapping is a no-op
    assert mapping_mod.invert(mapping) == mapping
    # lossless: legacy view -> invert reproduces the file exactly
    assert mapping_mod.invert(mapping_mod.revert(mapping)) == mapping
    # the consumer view equals the legacy 'fields' dict
    assert mapping_mod.entries(mapping) == mapping_mod.revert(mapping)["fields"]


@pytest.mark.parametrize("fid", FORM_IDS)
def test_bindings_carry_key_and_anchor_consistently(fid):
    mapping = json.loads((FORMS / fid / "mapping.json").read_text())
    for fid_key, binding in (mapping.get("map") or {}).items():
        assert binding.get("key"), f"{fid}: binding {fid_key!r} has no key"
        if "widgets" in binding:
            assert isinstance(binding["widgets"], list) and binding["widgets"]
            assert binding["widgets"][0] == fid_key, \
                f"{fid}: {fid_key!r} must anchor on its first widget"
        if binding.get("field_type") in mapping_mod.ENUM_GROUP_TYPES:
            options = binding.get("options") or {}
            assert fid_key in set(options.values()), \
                f"{fid}: enum group {fid_key!r} must anchor on an option widget"


def test_entries_raises_on_legacy_direction():
    with pytest.raises(ValueError):
        mapping_mod.entries({"form_id": "X", "fields": {
            "a.b": {"widget_id": "W", "field_type": "text"}}})


def test_invert_rejects_anchor_collision():
    with pytest.raises(ValueError):
        mapping_mod.invert({"form_id": "X", "fields": {
            "a.one": {"widget_id": "W", "field_type": "text"},
            "a.two": {"widget_id": "W", "field_type": "text"},
        }})


def test_invert_handles_every_binding_class():
    legacy = {"form_id": "X", "fields": {
        "a.text": {"widget_id": "T1", "field_type": "text",
                   "page": 0, "confidence": "high", "label": "A"},
        "a.fanout": {"widget_id": ["F1", "F2"], "field_type": "text"},
        "a.radio": {"widget_id": "grp", "field_type": "radio",
                    "options": {"x": "On1", "y": "On2"}},
        "a.enum": {"field_type": "enum_select",
                   "options": {"yes": "C1", "no": "C2"}},
        "a.name__gated": {"canonical_key": "a.name", "widget_id": "T2",
                          "field_type": "text", "when": "a.kind == 'g'"},
    }}
    canonical = mapping_mod.invert(legacy)
    m = canonical["map"]
    assert set(m) == {"T1", "F1", "grp", "C1", "T2"}
    assert m["F1"]["widgets"] == ["F1", "F2"]
    assert m["C1"]["options"] == {"yes": "C1", "no": "C2"}
    assert m["T2"]["canonical_key"] == "a.name"
    assert mapping_mod.revert(canonical) == legacy
    assert mapping_mod.entries(canonical) == legacy["fields"]
