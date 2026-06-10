"""engine.rubric — compile rubric prose into executable checks and evaluate.

Each test exercises one compiled rule pattern through a synthetic rubric, plus
the MANUAL_REVIEW passthrough and a repo-wide compile-coverage floor so the
compiler cannot silently regress against the real rubrics.
"""
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import rubric  # noqa: E402

TODAY = date(2026, 6, 10)
FORM_ID = "TEST_RUBRIC"


def _root(tmp_path, checks, schema=None):
    d = tmp_path / FORM_ID
    d.mkdir(exist_ok=True)
    (d / "rubric.yaml").write_text(yaml.safe_dump({"checks": checks}))
    if schema is not None:
        import json
        (d / "schema.json").write_text(json.dumps(schema))
    return str(tmp_path)


def _eval(tmp_path, checks, case, schema=None):
    return rubric.evaluate(FORM_ID, case, _root(tmp_path, checks, schema),
                           today=TODAY)


def _codes(result):
    return [i["code"] for i in result["issues"]]


# ---------------------------------------------------------------- non-empty

def test_nonempty_single_key(tmp_path):
    checks = [{"id": "name-required", "severity": "required",
               "description": "entity.name is non-empty.",
               "depends_on_keys": ["entity.name"]}]
    bad = _eval(tmp_path, checks, {"entity": {"name": " "}})
    assert _codes(bad) == ["MISSING_REQUIRED"] and not bad["ok"]
    assert bad["issues"][0]["severity"] == "error"
    assert bad["issues"][0]["rule_source"].endswith("#name-required")
    ok = _eval(tmp_path, checks, {"entity": {"name": "Acme LLC"}})
    assert ok["ok"] and not ok["issues"]


def test_nonempty_multi_key_with_parenthetical(tmp_path):
    checks = [{"id": "contact", "severity": "required",
               "description": "filing.contact.name, filing.contact.phone, "
                              "and filing.contact.email are non-empty "
                              "(cover-letter primitive).",
               "depends_on_keys": []}]
    bad = _eval(tmp_path, checks, {"filing": {"contact": {"name": "A"}}})
    assert _codes(bad) == ["MISSING_REQUIRED", "MISSING_REQUIRED"]


def test_nonempty_brace_group(tmp_path):
    checks = [{"id": "contact", "severity": "required",
               "description": "filing.contact.{name,phone,email} are all "
                              "non-empty."}]
    bad = _eval(tmp_path, checks, {})
    assert len(bad["issues"]) == 3


# -------------------------------------------------------------------- dates

def test_date_not_future(tmp_path):
    checks = [{"id": "dt", "severity": "required",
               "description": "filing.date_signed is non-empty and not in "
                              "the future."}]
    bad = _eval(tmp_path, checks, {"filing": {"date_signed": "2027-01-01"}})
    assert _codes(bad) == ["DATE_IN_FUTURE"]
    ok = _eval(tmp_path, checks, {"filing": {"date_signed": "2026-06-10"}})
    assert ok["ok"]


def test_date_order_on_or_after(tmp_path):
    checks = [{"id": "dt", "severity": "required",
               "description": "filing.date_signed is on or after "
                              "entity.maine_authorization_date."}]
    bad = _eval(tmp_path, checks, {
        "filing": {"date_signed": "2026-01-01"},
        "entity": {"maine_authorization_date": "2026-02-01"}})
    assert _codes(bad) == ["DATE_ORDER"]


def test_unparseable_date_is_warning(tmp_path):
    checks = [{"id": "dt", "severity": "required",
               "description": "filing.date_signed is non-empty and not in "
                              "the future."}]
    r = _eval(tmp_path, checks, {"filing": {"date_signed": "soonish"}})
    assert _codes(r) == ["UNPARSEABLE_DATE"]
    assert r["issues"][0]["severity"] == "warning"
    assert r["ok"]  # a warning never blocks


def test_date_formats_accepted(tmp_path):
    checks = [{"id": "dt", "severity": "required",
               "description": "filing.date_signed is not in the future."}]
    for v in ("2026-06-01", "06/01/2026", "June 1, 2026"):
        assert _eval(tmp_path, checks, {"filing": {"date_signed": v}})["ok"]


# ------------------------------------------------------- equality / differs

def test_matches_other_key(tmp_path):
    checks = [{"id": "match", "severity": "required",
               "description": "filing.entities[0].name matches "
                              "entity.name."}]
    bad = _eval(tmp_path, checks, {
        "filing": {"entities": [{"name": "A Corp"}]},
        "entity": {"name": "B Corp"}})
    assert _codes(bad) == ["VALUE_MISMATCH"]
    ok = _eval(tmp_path, checks, {
        "filing": {"entities": [{"name": "a corp"}]},
        "entity": {"name": "A Corp"}})
    assert ok["ok"]  # case-insensitive


def test_must_differ(tmp_path):
    checks = [{"id": "diff", "severity": "required",
               "description": "filing.terminated_fictitious_name is "
                              "different from entity.name."}]
    bad = _eval(tmp_path, checks, {
        "filing": {"terminated_fictitious_name": "Acme"},
        "entity": {"name": "ACME"}})
    assert _codes(bad) == ["VALUES_MUST_DIFFER"]


# ------------------------------------------------------------- enum choices

def test_exactly_one_enum_from_schema(tmp_path):
    schema = {"type": "object", "properties": {"registered_agent": {
        "type": "object", "properties": {"type": {
            "type": "string", "enum": ["commercial", "noncommercial"]}}}}}
    checks = [{"id": "ra-type", "severity": "required",
               "description": "Exactly one of FIFTH commercial/noncommercial "
                              "options is selected.",
               "depends_on_keys": ["registered_agent.type"]}]
    missing = _eval(tmp_path, checks, {}, schema)
    assert _codes(missing) == ["CHOICE_REQUIRED"]
    bad = _eval(tmp_path, checks,
                {"registered_agent": {"type": "imaginary"}}, schema)
    assert _codes(bad) == ["ENUM_INVALID"]
    ok = _eval(tmp_path, checks,
               {"registered_agent": {"type": "commercial"}}, schema)
    assert ok["ok"]


def test_exactly_one_inline_value_list(tmp_path):
    checks = [{"id": "exp", "severity": "required",
               "description": "filing.expedited_service is exactly one of "
                              "hold_for_pickup | 24h_next_business_day | "
                              "immediate_same_day.",
               "depends_on_keys": ["filing.expedited_service"]}]
    bad = _eval(tmp_path, checks, {"filing": {"expedited_service": "asap"}})
    assert _codes(bad) == ["ENUM_INVALID"]


def test_at_most_one_allows_absent(tmp_path):
    checks = [{"id": "exp", "severity": "required",
               "description": "At most one of the three expedite checkboxes "
                              "is selected.",
               "depends_on_keys": ["filing.expedited_service"]}]
    assert _eval(tmp_path, checks, {})["ok"]


# ------------------------------------------------------------- conditionals

def test_conditional_required_when_true(tmp_path):
    checks = [{"id": "prof", "severity": "required",
               "description": "If entity.is_professional_llc is true, "
                              "entity.professional_services_description "
                              "must be non-empty."}]
    bad = _eval(tmp_path, checks,
                {"entity": {"is_professional_llc": True}})
    assert _codes(bad) == ["CONDITIONAL_MISSING"]
    assert _eval(tmp_path, checks, {"entity": {}})["ok"]


def test_conditional_with_absent_branch(tmp_path):
    checks = [{"id": "cra", "severity": "required",
               "description": "If registered_agent.type = 'commercial', "
                              "registered_agent.cra_public_number must be "
                              "set; if 'noncommercial', it must be absent."}]
    bad1 = _eval(tmp_path, checks,
                 {"registered_agent": {"type": "commercial"}})
    assert _codes(bad1) == ["CONDITIONAL_MISSING"]
    bad2 = _eval(tmp_path, checks,
                 {"registered_agent": {"type": "noncommercial",
                                       "cra_public_number": "CRA1"}})
    assert _codes(bad2) == ["CONDITIONAL_FORBIDDEN"]
    ok = _eval(tmp_path, checks,
               {"registered_agent": {"type": "commercial",
                                     "cra_public_number": "CRA1"}})
    assert ok["ok"]


def test_conditional_date_with_it_subject(tmp_path):
    checks = [{"id": "fx", "severity": "required",
               "description": "If conversion.future_effective_date is set, "
                              "it must be on or after filing.date_signed."}]
    bad = _eval(tmp_path, checks, {
        "conversion": {"future_effective_date": "2026-01-01"},
        "filing": {"date_signed": "2026-02-01"}})
    assert _codes(bad) == ["DATE_ORDER"]


def test_conditional_must_be_true(tmp_path):
    checks = [{"id": "fict", "severity": "required",
               "description": "If entity.maine_fictitious_name is set, "
                              "filing.fict4_accompanies must be true."}]
    bad = _eval(tmp_path, checks,
                {"entity": {"maine_fictitious_name": "Acme of Maine"}})
    assert _codes(bad) == ["CONDITIONAL_MISSING"]


# ----------------------------------------------------- mutually exclusive

def test_mutually_exclusive_booleans(tmp_path):
    checks = [{"id": "mx", "severity": "required",
               "description": "entity.is_low_profit_llc and "
                              "entity.is_professional_llc cannot both be "
                              "true."}]
    bad = _eval(tmp_path, checks, {"entity": {"is_low_profit_llc": True,
                                              "is_professional_llc": True}})
    assert _codes(bad) == ["MUTUALLY_EXCLUSIVE"]
    assert _eval(tmp_path, checks,
                 {"entity": {"is_low_profit_llc": True}})["ok"]


# ------------------------------------------------------------ name suffixes

LLC_SUFFIX_DESC = (
    "entity.name ends with one of the statutory suffixes: 'Limited "
    "Liability Company', 'Limited Company', 'L.L.C.', 'LLC', 'L.C.', 'LC', "
    "or (if low-profit) 'L3C' or 'l3c' (case-insensitive substring match "
    "per 31 MRSA §1508)."
)


def test_llc_suffix_requirement(tmp_path):
    checks = [{"id": "suffix", "severity": "required",
               "description": LLC_SUFFIX_DESC,
               "depends_on_keys": ["entity.name",
                                   "entity.is_low_profit_llc"]}]
    bad = _eval(tmp_path, checks, {"entity": {"name": "Acme Corp."}})
    assert _codes(bad) == ["NAME_AFFIX_REQUIRED"]
    assert _eval(tmp_path, checks, {"entity": {"name": "Acme LLC"}})["ok"]
    # the L3C suffix only satisfies the check for a low-profit LLC
    plain_l3c = _eval(tmp_path, checks, {"entity": {"name": "Acme L3C"}})
    assert _codes(plain_l3c) == ["NAME_AFFIX_REQUIRED"]
    lp = _eval(tmp_path, checks, {"entity": {"name": "Acme L3C",
                                             "is_low_profit_llc": True}})
    assert lp["ok"]


def test_contains_statutory_suffix(tmp_path):
    checks = [{"id": "corp-suffix", "severity": "required",
               "description": "conversion.new_entity.name contains a "
                              "statutory corporate suffix per 13-C MRSA "
                              "§401: 'Corp.', 'Corporation', 'Co.', "
                              "'Company', 'Inc.', 'Incorporated', or "
                              "'Limited'."}]
    bad = _eval(tmp_path, checks,
                {"conversion": {"new_entity": {"name": "Acme LLC"}}})
    assert _codes(bad) == ["NAME_AFFIX_REQUIRED"]
    ok = _eval(tmp_path, checks,
               {"conversion": {"new_entity": {"name": "Acme Inc."}}})
    assert ok["ok"]


# ----------------------------------------------------------------- P.O. Box

def test_po_box_forbidden(tmp_path):
    checks = [{"id": "pobox", "severity": "required",
               "description": "registered_agent.physical_address is "
                              "non-empty and not a P.O. Box."}]
    for addr in ("P.O. Box 12", "PO Box 12", "Post Office Box 12"):
        bad = _eval(tmp_path, checks,
                    {"registered_agent": {"physical_address": addr}})
        assert _codes(bad) == ["PO_BOX_FORBIDDEN"], addr
    ok = _eval(tmp_path, checks,
               {"registered_agent": {"physical_address": "1 Main St"}})
    assert ok["ok"]


# ---------------------------------------------------------- forbidden value

def test_not_maine(tmp_path):
    checks = [{"id": "foreign", "severity": "required",
               "description": "entity.home_jurisdiction is not 'Maine' or "
                              "'ME' (foreign-qualification implies a "
                              "non-Maine home)."}]
    bad = _eval(tmp_path, checks, {"entity": {"home_jurisdiction": "maine"}})
    assert _codes(bad) == ["FORBIDDEN_VALUE"]
    assert _eval(tmp_path, checks,
                 {"entity": {"home_jurisdiction": "Vermont"}})["ok"]


# ------------------------------------------------------------------ formats

def test_email_format_conditional(tmp_path):
    checks = [{"id": "email", "severity": "optional",
               "description": "If entity.annual_report_reminder_email is "
                              "set, it must look like a valid email "
                              "address."}]
    bad = _eval(tmp_path, checks,
                {"entity": {"annual_report_reminder_email": "not-an-email"}})
    assert _codes(bad) == ["FORMAT_INVALID"]
    assert bad["issues"][0]["severity"] == "warning"  # optional -> warning


def test_single_uppercase_letter(tmp_path):
    checks = [{"id": "exhibit", "severity": "required",
               "description": "If entity.additional_provisions_exhibit_"
                              "letter is populated, it must be a single "
                              "uppercase letter A-Z."}]
    bad = _eval(tmp_path, checks,
                {"entity": {"additional_provisions_exhibit_letter": "a1"}})
    assert _codes(bad) == ["FORMAT_INVALID"]
    assert _eval(tmp_path, checks,
                 {"entity": {"additional_provisions_exhibit_letter": "B"}}
                 )["ok"]


# --------------------------------------------------------------------- fees

FEE_DESC = ("filing.total_fees_dollars equals $35 base fee plus any "
            "expedite premium ($50 for 24h_next_business_day, $100 for "
            "immediate_same_day, $0 for hold_for_pickup).")


def test_fee_base_plus_expedite(tmp_path):
    checks = [{"id": "fee", "severity": "optional",
               "description": FEE_DESC,
               "depends_on_keys": ["filing.total_fees_dollars",
                                   "filing.expedited_service"]}]
    ok = _eval(tmp_path, checks, {"filing": {"total_fees_dollars": "$35"}})
    assert ok["ok"] and not ok["issues"]
    ok2 = _eval(tmp_path, checks, {"filing": {
        "total_fees_dollars": 135,
        "expedited_service": "immediate_same_day"}})
    assert ok2["ok"]
    bad = _eval(tmp_path, checks, {"filing": {
        "total_fees_dollars": 35,
        "expedited_service": "immediate_same_day"}})
    assert _codes(bad) == ["FEE_MISMATCH"]
    # no asserted total -> nothing to check
    assert _eval(tmp_path, checks, {"filing": {}})["ok"]


# ------------------------------------------------------------ signer blocks

def test_exactly_one_signer_block(tmp_path):
    checks = [{"id": "sb", "severity": "required",
               "description": "Exactly one signer block is populated: "
                              "either filing.signer.printed_name_and_"
                              "capacity (individual partner) OR (filing."
                              "signer_entity.name AND filing.signer_entity."
                              "signer_printed_name_and_capacity) (entity "
                              "partner). Both blocks empty or both "
                              "populated is a fill error."}]
    empty = _eval(tmp_path, checks, {})
    assert _codes(empty) == ["SIGNER_BLOCK_REQUIRED"]
    both = _eval(tmp_path, checks, {"filing": {
        "signer": {"printed_name_and_capacity": "A, Partner"},
        "signer_entity": {"name": "B LLC",
                          "signer_printed_name_and_capacity": "C, Mgr"}}})
    assert _codes(both) == ["MULTIPLE_BLOCKS_POPULATED"]
    one = _eval(tmp_path, checks, {"filing": {
        "signer": {"printed_name_and_capacity": "A, Partner"}}})
    assert one["ok"]


def test_at_least_one_of(tmp_path):
    checks = [{"id": "alo", "severity": "required",
               "description": "At least one of filing.signer or "
                              "filing.signer_2 printed_name_and_capacity "
                              "is non-empty.",
               "depends_on_keys": [
                   "filing.signer.printed_name_and_capacity",
                   "filing.signer_2.printed_name_and_capacity"]}]
    bad = _eval(tmp_path, checks, {})
    assert _codes(bad) == ["AT_LEAST_ONE_REQUIRED"]
    ok = _eval(tmp_path, checks, {"filing": {
        "signer_2": {"printed_name_and_capacity": "B, Member"}}})
    assert ok["ok"]


# ---------------------------------------------------------- roster pairing

def test_name_address_pairs(tmp_path):
    checks = [{"id": "pairs", "severity": "required",
               "description": "Every populated officer_<role>.name has a "
                              "corresponding officer_<role>.address (and "
                              "likewise for director_N).",
               "depends_on_keys": ["officer_president.name",
                                   "officer_president.address",
                                   "director_1.name",
                                   "director_1.address"]}]
    bad = _eval(tmp_path, checks,
                {"officer_president": {"name": "Pat President"}})
    assert _codes(bad) == ["PAIRED_FIELDS_INCOMPLETE"]
    ok = _eval(tmp_path, checks,
               {"officer_president": {"name": "Pat", "address": "1 Main"}})
    assert ok["ok"]


# --------------------------------------------------- manual-review fallback

def test_manual_review_passthrough(tmp_path):
    prose = ("EIGHTH paragraph requires that an attached certificate of "
             "existence is dated within 90 days before delivery; tracked "
             "manually in filing.notes.")
    checks = [{"id": "coe", "severity": "required", "description": prose,
               "depends_on_keys": []}]
    r = _eval(tmp_path, checks, {})
    assert _codes(r) == ["MANUAL_REVIEW"]
    issue = r["issues"][0]
    assert issue["severity"] == "manual"
    assert issue["message"] == prose  # prose passed through, never dropped
    assert r["ok"]  # manual review does not block
    assert r["stats"] == {"checks": 1, "machine_evaluated": 0,
                          "manual_review": 1}


def test_row_template_keys_stay_manual(tmp_path):
    # "_N" row templates cannot be grounded against a case — keep manual
    checks = [{"id": "rows", "severity": "required",
               "description": "If partner_entity_N.name is populated, "
                              "partner_entity_N.signer_printed_name_and_"
                              "capacity must also be populated."}]
    r = _eval(tmp_path, checks, {"partner_entity_1": {"name": "X"}})
    assert _codes(r) == ["MANUAL_REVIEW"]


# ------------------------------------------------------------- repo-wide

def test_missing_rubric_is_empty(tmp_path):
    (tmp_path / "NO_RUBRIC").mkdir()
    r = rubric.evaluate("NO_RUBRIC", {}, str(tmp_path))
    assert r["ok"] and r["issues"] == [] and r["stats"]["checks"] == 0


def test_repo_rubrics_compile_coverage_floor():
    cov = rubric.coverage(str(ROOT / "forms"))
    assert cov["total_checks"] > 1500
    rate = cov["machine_evaluated"] / cov["total_checks"]
    assert rate >= 0.75, (
        f"rubric compile coverage regressed to {rate:.1%}; "
        "see python -m engine.rubric --coverage --unmatched")


def test_repo_rubrics_evaluate_without_crashing():
    # every form's rubric must evaluate against an empty and a junk case
    for d in sorted((ROOT / "forms").iterdir()):
        if not (d / "rubric.yaml").exists():
            continue
        for case in ({}, {"entity": {"name": 7}, "filing": "oops"}):
            r = rubric.evaluate(d.name, case if isinstance(case, dict)
                                else {}, str(ROOT / "forms"), today=TODAY)
            assert isinstance(r["issues"], list)
