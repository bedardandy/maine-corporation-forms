"""Signer-rule classification, capacity normalization, and case validation."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import signer_rules  # noqa: E402


# ---- formation vs other classification --------------------------------------

def test_name_registration_forms_are_not_formations():
    # "Application for Registration of Name" / "Consent Terminating Name
    # Registration" are filings by an *existing* foreign entity, signed by an
    # officer — a bare "registration" title token must not class them as
    # formations with incorporator-only capacities.
    for fid in ("CORP_MBCA-2", "CORP_MBCA-2A"):
        caps = signer_rules.rules_for(fid)["allowed_signer_capacities"]
        assert "officer" in caps, f"{fid}: {caps}"
    caps = signer_rules.rules_for("NP_MNPCA-2")["allowed_signer_capacities"]
    assert "officer" in caps


def test_true_formation_still_classed():
    assert signer_rules.rules_for("CORP_MBCA-6")[
        "allowed_signer_capacities"] == ["incorporator"]


def test_catalog_matches_generator():
    catalog = json.loads(
        (ROOT / "catalog" / "signer_rules.json").read_text())
    for fid in ("CORP_MBCA-2", "CORP_MBCA-2A", "NP_MNPCA-2", "CORP_MBCA-6"):
        assert catalog[fid] == signer_rules.rules_for(fid)


# ---- capacity normalization --------------------------------------------------

def test_normalize_word_boundary_not_substring():
    n = signer_rules.normalize_capacity
    assert n("principal") == "principal"          # not "inc" -> incorporator
    assert n("managing agent") == "managing agent"  # not registered agent
    assert n("sole incorporator") == "incorporator"
    assert n("managing member") == "member"
    assert n("Vice President") == "officer"
    assert n("registered agent for the entity") == "registered agent"


def test_normalize_longest_token_first():
    assert signer_rules.normalize_capacity(
        "duly authorized general partner") == "general partner"


# ---- entity_class ------------------------------------------------------------

def test_entity_class_unknown_prefix_is_none():
    assert signer_rules.entity_class("ZZZ_1") is None
    rules = signer_rules.rules_for("ZZZ_1")
    assert rules["source"] != "default"
    assert "unrecognized" in rules["source"]


# ---- validate resolves the canonical filing.signer block ----------------------

def test_validate_reads_filing_signer():
    case = {"filing": {"signer": {"printed_name": "Marguerite Example",
                                  "capacity": "Authorized Member"}}}
    assert signer_rules.validate("LLC_MLLC-6", case) == []


def test_validate_reads_combined_name_and_capacity():
    case = {"filing": {"signer": {
        "printed_name_and_capacity": "Jane Doe, Manager"}}}
    assert signer_rules.validate("LLC_MLLC-6", case) == []


def test_validate_flags_disallowed_capacity():
    case = {"filing": {"signer": {"printed_name": "P. Example",
                                  "capacity": "President"}}}
    issues = signer_rules.validate("CORP_MBCA-6", case)  # formation: incorporator
    assert any(i["code"] == "capacity-not-allowed" for i in issues)


def test_validate_warns_without_signature_block():
    issues = signer_rules.validate("LLC_MLLC-6", {})
    assert issues and issues[0]["code"] == "no-signature-block"
