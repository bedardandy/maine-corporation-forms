"""registered_agent.type is a real selection on every form that carries it.

Pins the checkbox-fan sweep: the migration-era mappings carried the
text-typed ``registered_agent.type`` fanned onto checkbox widgets, so the
filler wrote the literal type string into the button ``/V`` and the box was
never selected. Every binding of the key is now a ``radio`` (same-named
button group with distinct kid on-states; the deterministic radio post-pass
selects it) or an ``enum_select`` (independently named checkboxes, each
on-state ``Yes``; the chosen widget is checked, every sibling forced off).
Canonical values follow the blanks' printed options ("Commercial Registered
Agent" / "Noncommercial Registered Agent") on all 21 forms.

These tests are pure mapping/schema/resolution checks — no blank PDF is
opened. tools/equivalence_check.py records the same forms as intentional
divergences from the frozen pypdf baseline.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import fill  # noqa: E402
from engine.mapping import entries as mapping_entries  # noqa: E402

FORMS = ROOT / "forms"
KEY = "registered_agent.type"
ENUM = ["commercial", "noncommercial"]

#: form -> (field_type, anchor/group, expected per-value selection target:
#: the checked widget for enum_select, the group on-state for radio).
EXPECTED = {
    "CORP_MBCA-12": ("enum_select", {"commercial": "Check Box2",
                                     "noncommercial": "Check Box1"}),
    "LLC_MLLC-6": ("enum_select", {"commercial": "Check Box8",
                                   "noncommercial": "Check Box12"}),
    "LLC_MLLC-6A": ("enum_select", {"commercial": "Check Box7",
                                    "noncommercial": "Check Box8"}),
    "LLC_MLLC-9": ("enum_select", {"commercial": "Check Box8",
                                   "noncommercial": "Check Box9"}),
    "LLC_MLLC-12": ("enum_select", {"commercial": "Check Box15",
                                    "noncommercial": "Check Box16"}),
    "LLC_MLLC-12A": ("enum_select", {"commercial": "Check Box16__p1",
                                     "noncommercial": "Check Box18"}),
    "LLP_MLLP-6": ("enum_select", {"commercial": "Check Box22",
                                   "noncommercial": "Check Box23"}),
    "LLP_MLLP-6-1": ("enum_select", {"commercial": "Check Box17",
                                     "noncommercial": "Check Box18"}),
    "LLP_MLLP-6A": ("enum_select", {"commercial": "Check Box20",
                                    "noncommercial": "Check Box21"}),
    "LLP_MLLP-12": ("enum_select", {"commercial": "Check Box24",
                                    "noncommercial": "Check Box25"}),
    "LLP_MLLP-12-1": ("enum_select", {"commercial": "Check Box20",
                                      "noncommercial": "Check Box21"}),
    "LP_MLPA-6": ("enum_select", {"commercial": "Check Box29",
                                  "noncommercial": "Check Box30"}),
    "LP_MLPA-6-1": ("enum_select", {"commercial": "Check Box24",
                                    "noncommercial": "Check Box25"}),
    "LP_MLPA-6A": ("enum_select", {"commercial": "Check Box5",
                                   "noncommercial": "Check Box6"}),
    "LP_MLPA-12": ("enum_select", {"commercial": "Check Box29",
                                   "noncommercial": "Check Box30"}),
    "LP_MLPA-12-1": ("enum_select", {"commercial": "Check Box26",
                                     "noncommercial": "Check Box27"}),
    "NP_MNPCA-6": ("radio", {"commercial": "Yes",
                             "noncommercial": "cra2"}),
    "NP_MNPCA-6-1": ("enum_select", {"commercial": "Check Box12",
                                     "noncommercial": "Check Box13"}),
    "NP_MNPCA-12": ("enum_select", {"commercial": "Check Box20",
                                    "noncommercial": "Check Box21"}),
    "NP_MNPCA-12-1": ("enum_select", {"commercial": "Check Box4",
                                      "noncommercial": "Check Box5"}),
    "NP_MNPCA-6A_0": ("enum_select", {"commercial": "Check Box9",
                                      "noncommercial": "Check Box10"}),
}


def _binding(fid):
    mapping = json.loads((FORMS / fid / "mapping.json").read_text())
    hits = [(anchor, spec) for anchor, spec in mapping["map"].items()
            if isinstance(spec, dict) and spec.get("key") == KEY]
    assert len(hits) == 1, f"{fid}: expected exactly one {KEY} binding"
    return hits[0]


def test_expected_covers_every_form_with_the_key():
    # No form binds registered_agent.type outside the pinned set, and none
    # regressed to a text fan-out over checkbox widgets.
    carrying = set()
    for d in sorted(FORMS.iterdir()):
        mapping = json.loads((d / "mapping.json").read_text())
        for spec in (mapping.get("map") or {}).values():
            if isinstance(spec, dict) and spec.get("key") == KEY:
                carrying.add(d.name)
    assert carrying == set(EXPECTED)


@pytest.mark.parametrize("fid", sorted(EXPECTED))
def test_binding_is_a_selection_with_the_printed_options(fid):
    field_type, options = EXPECTED[fid]
    anchor, spec = _binding(fid)
    assert spec.get("field_type") == field_type
    assert spec.get("options") == options
    if field_type == "enum_select":
        # the canonical-direction anchor is the first option widget
        assert anchor == next(iter(spec["options"].values()))
        assert "widgets" not in spec  # the fan-out list is gone


@pytest.mark.parametrize("fid", sorted(EXPECTED))
def test_schema_pins_the_enum(fid):
    schema = json.loads((FORMS / fid / "schema.json").read_text())
    node = schema["properties"]["registered_agent"]["properties"]["type"]
    assert node.get("enum") == ENUM


@pytest.mark.parametrize("fid", sorted(EXPECTED))
@pytest.mark.parametrize("value", ENUM)
def test_resolution_selects_exactly_one(fid, value):
    field_type, expected = EXPECTED[fid]
    report = {}
    plan = fill.resolve_fill(fid, {"registered_agent": {"type": value}},
                             str(FORMS), report=report)
    assert report["dropped_enums"] == []
    if field_type == "radio":
        anchor, _ = _binding(fid)
        assert (anchor, expected[value]) in plan["radio_selections"]
    else:
        _, options = EXPECTED[fid]
        chosen = expected[value]
        assert plan["field_data"][chosen] == "Yes"
        for sibling in options.values():
            if sibling != chosen:
                assert plan["field_data"][sibling] == ""


def test_unmapped_value_is_reported_not_written():
    report = {}
    plan = fill.resolve_fill("LLP_MLLP-6",
                             {"registered_agent": {"type": "hybrid"}},
                             str(FORMS), report=report)
    assert report["dropped_enums"] == [
        {"key": "registered_agent.type", "value": "hybrid",
         "allowed": ["commercial", "noncommercial"]}]
    for widget in EXPECTED["LLP_MLLP-6"][1].values():
        assert widget not in plan["field_data"]
