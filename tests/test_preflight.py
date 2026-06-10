"""engine.preflight — one merged issue list from schema+rubric+signer+plan."""
import io
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import preflight  # noqa: E402
from engine.preflight import PreflightError  # noqa: E402

FORM_ID = "LLC_MLLC-6"


def _case(name):
    return json.loads((ROOT / "examples" / name).read_text())


def test_curated_llc_example_passes_clean():
    r = preflight.preflight(FORM_ID, _case("llc_mllc-6.case.json"),
                            str(ROOT / "forms"))
    assert r["ok"]
    assert r["summary"]["error"] == 0
    assert r["coverage"] is not None


def test_curated_corp_example_passes_clean():
    r = preflight.preflight("CORP_MBCA-6", _case("corp_mbca-6.case.json"),
                            str(ROOT / "forms"))
    assert r["ok"], [i["message"] for i in r["issues"]
                     if i["severity"] == "error"]


def test_curated_np_example_passes_clean():
    r = preflight.preflight("NP_MNP-981A", _case("np_mnp-981a.case.json"),
                            str(ROOT / "forms"))
    assert r["ok"], [i["message"] for i in r["issues"]
                     if i["severity"] == "error"]


def test_issue_shape_and_sources():
    case = _case("llc_mllc-6.case.json")
    case["entity"]["name"] = "Wabanaki Widgets"  # drop the LLC suffix
    case["registered_agent"]["physical_address"] = "P.O. Box 4"
    r = preflight.preflight(FORM_ID, case, str(ROOT / "forms"))
    assert not r["ok"]
    codes = {i["code"] for i in r["issues"]}
    assert "NAME_AFFIX_REQUIRED" in codes
    assert "PO_BOX_FORBIDDEN" in codes
    for i in r["issues"]:
        assert i["source"] in ("schema", "rubric", "signer", "plan")
        assert i["severity"] in ("error", "warning", "info", "manual")
        assert set(i) >= {"source", "code", "severity", "keys", "message"}
    s = r["summary"]
    assert s["error"] == sum(1 for i in r["issues"]
                             if i["severity"] == "error")


def test_schema_violation_is_error():
    case = _case("llc_mllc-6.case.json")
    case["entity"]["is_low_profit_llc"] = "yes-ish"  # boolean per schema
    r = preflight.preflight(FORM_ID, case, str(ROOT / "forms"))
    assert any(i["source"] == "schema" and i["severity"] == "error"
               for i in r["issues"])
    assert not r["ok"]


def test_unknown_form_fails_closed():
    r = preflight.preflight("NO_SUCH_FORM", {}, str(ROOT / "forms"))
    assert not r["ok"]
    assert any(i["code"] == "PLAN_FAILED" for i in r["issues"])


def test_non_dict_case_fails_closed():
    r = preflight.preflight(FORM_ID, ["not", "a", "case"],
                            str(ROOT / "forms"))
    assert not r["ok"] and r["issues"][0]["code"] == "CASE_NOT_OBJECT"


def test_manual_rubric_checks_do_not_block():
    r = preflight.preflight(FORM_ID, _case("llc_mllc-6.case.json"),
                            str(ROOT / "forms"))
    assert r["ok"]
    # MLLC-6 carries at least one human-judgment check — it must be
    # surfaced as severity=manual, not dropped and not blocking
    assert r["summary"]["manual"] >= 1
    assert all(i["source"] == "rubric"
               for i in r["issues"] if i["severity"] == "manual")


def test_plan_required_flag_is_warning_not_error(tmp_path):
    # the plan's "referenced by a required check" approximation must not
    # block a case the (conditional-aware) rubric accepts
    d = tmp_path / "T1"
    d.mkdir()
    (d / "mapping.json").write_text(json.dumps({"fields": {
        "a.flag": {"field_type": "checkbox", "widget_id": "F"},
        "a.detail": {"field_type": "text", "widget_id": "D"},
    }}))
    (d / "rubric.yaml").write_text(yaml.safe_dump({"checks": [{
        "id": "detail-when-flagged", "severity": "required",
        "description": "If a.flag is true, a.detail must be non-empty.",
        "depends_on_keys": ["a.flag", "a.detail"]}]}))
    r = preflight.preflight("T1", {"a": {}}, str(tmp_path))
    assert r["ok"]
    plan_issues = [i for i in r["issues"] if i["source"] == "plan"]
    assert all(i["severity"] != "error" for i in plan_issues)


def test_fill_gate_blocks_on_error_and_no_preflight_overrides(tmp_path):
    # reuse the synthetic-blank helper from the fill tests
    sys.path.insert(0, str(ROOT / "tests"))
    from test_fill import _make_blank
    from engine import fill

    d = tmp_path / "TGATE"
    d.mkdir()
    _make_blank(d / "TGATE.pdf", ["NameField"])
    (d / "mapping.json").write_text(json.dumps({"fields": {
        "entity.name": {"field_type": "text", "widget_id": "NameField"},
    }}))
    (d / "rubric.yaml").write_text(yaml.safe_dump({"checks": [{
        "id": "name-required", "severity": "required",
        "description": "entity.name is non-empty.",
        "depends_on_keys": ["entity.name"]}]}))

    with pytest.raises(PreflightError) as exc:
        fill.fill_to_stream("TGATE", {}, io.BytesIO(), str(tmp_path),
                            verify_blank="off")
    assert exc.value.result["summary"]["error"] >= 1

    report = {}
    fill.fill_to_stream("TGATE", {}, io.BytesIO(), str(tmp_path),
                        verify_blank="off", report=report, preflight="off")
    assert "preflight" not in report  # gate skipped entirely

    # a passing case fills and carries the preflight result in the report
    report = {}
    fill.fill_to_stream("TGATE", {"entity": {"name": "Acme LLC"}},
                        io.BytesIO(), str(tmp_path), verify_blank="off",
                        report=report)
    assert report["preflight"]["ok"]


def test_fill_gate_rejects_bad_mode():
    from engine import fill
    with pytest.raises(ValueError):
        fill._preflight_mode("loose")


def test_cli_exit_codes(tmp_path):
    import subprocess
    case = tmp_path / "case.json"
    case.write_text(json.dumps(_case("llc_mllc-6.case.json")))
    ok = subprocess.run(
        [sys.executable, "-m", "engine.preflight", FORM_ID, str(case)],
        cwd=ROOT, capture_output=True, text=True)
    assert ok.returncode == 0 and "OK" in ok.stdout
    case.write_text("{}")
    bad = subprocess.run(
        [sys.executable, "-m", "engine.preflight", FORM_ID, str(case),
         "--json"],
        cwd=ROOT, capture_output=True, text=True)
    assert bad.returncode == 1
    payload = json.loads(bad.stdout)
    assert payload["ok"] is False and payload["summary"]["error"] >= 1
