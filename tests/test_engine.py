"""Engine logic that needs no blank PDF: routing, planning, schema validation."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import plan, route, schema  # noqa: E402

EXAMPLES = {
    "CORP_MBCA-6": "corp_mbca-6.case.json",
    "LLC_MLLC-6": "llc_mllc-6.case.json",
    "NP_MNP-981A": "np_mnp-981a.case.json",
}


def _case(name):
    return json.loads((ROOT / "examples" / name).read_text())


def test_route_returns_candidates():
    hits = route.route("convert a limited liability company to a corporation",
                       str(ROOT / "catalog"))
    assert hits and all(len(h) == 3 for h in hits)


@pytest.mark.parametrize("fid,case_file", EXAMPLES.items())
def test_example_validates_clean(fid, case_file):
    assert schema.validate(fid, _case(case_file), str(ROOT / "forms")) == []


@pytest.mark.parametrize("fid,case_file", EXAMPLES.items())
def test_plan_buckets_partition_fields(fid, case_file):
    p = plan.build_plan(fid, _case(case_file), str(ROOT / "forms"))
    assert p["ok"]
    c = p["coverage"]
    assert c["resolved"] + c["unresolved"] + c["skipped"] == p["n_fields"]
    assert c["resolved"] > 0


def test_mllc6_agent_name_gated_by_type():
    # The MLLC-6 agent-name line is split: Text11 (commercial) and Text13
    # (noncommercial) are separate when-gated entries over one canonical key,
    # so only the row matching registered_agent.type fills.
    case = _case("llc_mllc-6.case.json")
    assert case["registered_agent"]["type"] == "noncommercial"
    p = plan.build_plan("LLC_MLLC-6", case, str(ROOT / "forms"))
    assert "registered_agent.name__noncommercial" in p["resolved"]
    assert "registered_agent.name__commercial" in {
        s["key"] for s in p["skipped"]}


def test_mllc6_signer_key_is_canonical():
    # Guards the printed_name_and_capacity rename (was *_and_title, which a
    # conforming case never sets, leaving the signer line blank).
    case = _case("llc_mllc-6.case.json")
    p = plan.build_plan("LLC_MLLC-6", case, str(ROOT / "forms"))
    assert "filing.signer.printed_name_and_capacity" in p["resolved"]


def test_plan_absent_boolean_is_not_required_missing():
    # entity.is_low_profit_llc is referenced by required rubric checks, but a
    # clean MLLC-6 case that omits it just means "not an L3C" — it must not be
    # reported as a blocking missing fact.
    case = _case("llc_mllc-6.case.json")
    assert "is_low_profit_llc" not in case["entity"]
    p = plan.build_plan("LLC_MLLC-6", case, str(ROOT / "forms"))
    flagged = {u["key"] for u in p["unresolved"] if u["required"]}
    assert "entity.is_low_profit_llc" not in flagged
    # it is still listed as unresolved (an optional fact), just not blocking
    assert "entity.is_low_profit_llc" in {u["key"] for u in p["unresolved"]}


def test_plan_surfaces_unmapped_enum_values():
    case = _case("llc_mllc-6.case.json")
    case["registered_agent"]["type"] = "hybrid"  # not a mapped option
    p = plan.build_plan("LLC_MLLC-6", case, str(ROOT / "forms"))
    assert {"key": "registered_agent.type", "value": "hybrid",
            "allowed": ["commercial", "noncommercial"]} in p["unmapped_enums"]


def test_plan_rejects_non_object_case():
    p = plan.build_plan("CORP_MBCA-6", ["not", "a", "dict"], str(ROOT / "forms"))
    assert p["ok"] is False


def test_plan_unknown_form():
    p = plan.build_plan("NOPE_404", {}, str(ROOT / "forms"))
    assert p["ok"] is False
