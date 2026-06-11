"""MCP payload builders in tools/agent_server.py (no mcp dependency needed).

get_form must give an agent enough context to act safely — trust/confidence
summary, printed fee, workflow membership, preflight hint — while staying
bounded (~4KB) so it never floods a tool transcript.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import agent_server  # noqa: E402

MAX_PAYLOAD_BYTES = 4096


def _form_ids():
    index = json.loads((ROOT / "catalog" / "forms_index.json").read_text())
    return [f["form_id"] for f in index["forms"]]


def test_get_form_unknown_id_is_an_error_not_a_crash():
    assert "error" in agent_server.get_form_payload("NOT_A_FORM")


def test_get_form_payload_bounded_for_every_form():
    for fid in _form_ids():
        payload = agent_server.get_form_payload(fid)
        assert "error" not in payload, fid
        assert len(json.dumps(payload)) <= MAX_PAYLOAD_BYTES, fid


def test_get_form_payload_keys_and_trust_summary():
    p = agent_server.get_form_payload("CORP_MBCA-6A")
    assert {"form_id", "title", "entity_type", "statute", "n_fields",
            "trust", "fee", "workflows", "preflight",
            "not_legal_advice"} <= set(p)
    trust = p["trust"]
    assert sum(trust["confidence"].values()) == p["n_fields"]
    assert len(trust["unverified_fields"]) <= agent_server._MAX_UNVERIFIED
    # below-high-confidence fields are surfaced, high-confidence ones aren't
    mapping = json.loads(
        (ROOT / "forms" / "CORP_MBCA-6A" / "mapping.json").read_text())
    from engine.mapping import entries as mapping_entries
    expect = sorted(k for k, s in mapping_entries(mapping).items()
                    if s.get("confidence") != "high")
    assert trust["unverified_fields"] == expect[:agent_server._MAX_UNVERIFIED]


def test_get_form_fee_matches_catalog():
    fees = json.loads((ROOT / "catalog" / "fees.json").read_text())["fees"]
    for fid in ("CORP_MBCA-6", "CORP_MBCA-6-1", "NP_MNPCA-16"):
        assert agent_server.get_form_payload(fid)["fee"] == fees[fid]


def test_get_form_workflow_membership_matches_catalog():
    p = agent_server.get_form_payload("CORP_MBCA-6A")
    assert {"id": "corp_restated_articles",
            "title": "Restate the articles of a Maine business corporation",
            "required": True} in p["workflows"]
    # the companion cover sheet belongs to several workflows
    cover = agent_server.get_form_payload("CORP_MBCA-6-1")
    ids = {w["id"] for w in cover["workflows"]}
    assert "corp_restated_articles" in ids and len(ids) >= 4


def test_find_forms_results_carry_workflow_ids(monkeypatch):
    # force the offline lexical fallback so the test is deterministic
    monkeypatch.setenv("ROUTER_BASE_URL", "http://127.0.0.1:9")
    results = agent_server.find_forms_payload(
        "merger where the survivor is a corporation", 5)
    assert results
    assert all("workflows" in r for r in results)
    by_id = {r["form_id"]: r for r in results}
    if "CORP_MBCA-10" in by_id:
        assert "corp_merger_share_exchange" in by_id["CORP_MBCA-10"][
            "workflows"]
