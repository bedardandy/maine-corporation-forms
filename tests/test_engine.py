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


def test_plan_rejects_non_object_case():
    p = plan.build_plan("CORP_MBCA-6", ["not", "a", "dict"], str(ROOT / "forms"))
    assert p["ok"] is False


def test_plan_unknown_form():
    p = plan.build_plan("NOPE_404", {}, str(ROOT / "forms"))
    assert p["ok"] is False
