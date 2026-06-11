"""Every fact key the /Btn sweep re-bound is a real selection.

Pins the repo-wide non-boolean-key-on-button-widgets sweep (the follow-up to
the registered_agent.type sweep in tests/test_registered_agent_type.py): the
migration-era mappings carried text-typed fact keys fanned onto checkbox
widgets, so the filler wrote the literal enum string into the button ``/V``
and no box was ever selected. Every such binding is now an ``enum_select``
(independently named checkboxes, each on-state ``Yes``; the chosen widget is
checked, every sibling forced off) with values pinned from the blanks'
printed option labels, or a plain ``checkbox`` boolean where the blank has a
single yes/this-applies box. Promoted ``<T>__p<page>`` names address the kids
of shared multi-page /Btn fields (engine.field_split).

These tests are pure mapping/schema/resolution checks except the final
structural scan, which opens every blank and asserts the smell class cannot
regress anywhere in the repo. tools/equivalence_check.py records the same
forms as intentional divergences from the frozen pypdf baseline.
"""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import fill  # noqa: E402

FORMS = ROOT / "forms"

#: (form, key) -> enum_select options (enum value -> checked widget), in the
#: blank's printed option order; the anchor is the first option's widget.
ENUM_SELECTS = {
    ("CORP_MBCA-11I", "dissolution.early_dissolution_basis"): {
        "no_shares_issued": "Check Box4",
        "not_commenced_business": "Check Box5"},
    ("CORP_MBCA-12C", "transfer.new_entity_type"): {
        "foreign_nonprofit_corporation": "Check Box1",
        "foreign_limited_partnership": "Check Box2",
        "foreign_limited_liability_company": "Check Box3",
        "foreign_limited_liability_partnership": "Check Box4"},
    ("CORP_MBCA-14A", "resumption.method"): {
        "meeting": "Check Box4",
        "written_consent": "Check Box5"},
    ("CORP_MBCA-19B", "abandonment.path"): {
        "domestic": "Check Box4",
        "foreign": "Check Box5"},
    ("CORP_MBCA-6A", "amendment.approval_method"): {
        "incorporators": "Check Box10",
        "board_of_directors": "Check Box11",
        "shareholders": "Check Box13"},
    ("LLC_MLLC-10", "merger.third_subelection"): {
        "amendments_attached": "Check Box14__p0",
        "organizational_docs_unchanged": "Check Box15__p0"},
    ("LLC_MLLC-2", "filing.application_type"): {
        "new": "Check Box2",
        "renewal": "Check Box3"},
    ("LLC_MLLCACSOA", "filing.action_type"): {
        "amendment": "Check Box3",
        "cancellation": "Check Box9"},
    ("LLC_MLLCCONV", "conversion.organizing_document_disposition"): {
        "attached_as_exhibit": "Check Box3",
        "not_filing_with_sos": "Check Box5"},
    ("LLP_MLLP-6-1", "filing.underlying_filing_type"): {
        "articles_of_entity_conversion": "Check Box12",
        "merger_or_share_exchange": "Check Box13",
        "inter_entity_consolidation": "Check Box14",
        "articles_of_conversion": "Check Box15",
        "conversion_of_partnership": "Check Box16"},
    ("LP_MLPA-10", "merger.fifth_election"): {
        "created_by_merger": "Check Box21",
        "preexisted": "Check Box22"},
    ("LP_MLPA-10", "merger.fifth_subelection"): {
        "amendments_attached": "Check Box23",
        "organizational_docs_unchanged": "Check Box24"},
    ("LP_MLPA-2", "filing.application_type"): {
        "new": "Check Box2",
        "renewal": "Check Box3"},
    ("MARK_mark1", "mark.applicant.entity_type"): {
        "individual": "Check Box23",
        "general_partnership": "Check Box32",
        "limited_partnership": "Check Box25",
        "corporation": "Check Box26",
        "association": "Check Box27",
        "union": "Check Box28",
        "other": "Check Box31"},
    ("MARK_mark1a", "mark.type"): {
        "trademark": "Check Box9",
        "service_mark": "Check Box10",
        "combined_service_trademark": "Check Box11",
        "certification_mark": "Check Box12",
        "collective_mark": "Check Box13"},
    ("MARK_mark2", "mark.class_changes[0].action"): {
        "added": "Check Box7",
        "deleted": "Check Box8"},
    ("MARK_mark2", "mark.applicant.entity_type"): {
        "individual": "Check Box10",
        "general_partnership": "Check Box11",
        "limited_partnership": "Check Box12",
        "corporation": "Check Box15__p1",
        "association": "Check Box16__p1",
        "union": "Check Box17",
        "other": "Check Box18"},
    ("MARK_mark3", "amendment.class_action"): {
        "added": "Check Box6",
        "deleted": "Check Box7"},
    ("MARK_mark3", "mark.applicant.entity_type"): {
        "individual": "Check Box9",
        "general_partnership": "Check Box10",
        "limited_partnership": "Check Box11",
        "corporation": "Check Box12",
        "association": "Check Box16__p1",
        "union": "Check Box13",
        "other": "Check Box17"},
    ("MARK_mark4", "mark.assignor.entity_type"): {
        "individual": "Check Box4",
        "general_partnership": "Check Box5",
        "limited_partnership": "Check Box6",
        "corporation": "Check Box7",
        "association": "Check Box8",
        "union": "Check Box9",
        "other": "Check Box10"},
    ("MARK_mark4", "mark.assignee.entity_type"): {
        "individual": "Check Box11",
        "general_partnership": "Check Box12",
        "limited_partnership": "Check Box13",
        "corporation": "Check Box14__p1",
        "association": "Check Box15__p1",
        "union": "Check Box16__p1",
        "other": "Check Box17"},
    ("NP_CLKRA-3", "clerk_change.action_type"): {
        "new_appointment": "Check Box1",
        "modify_existing": "Check Box2"},
    ("NP_CLKRA-3", "clerk_change.modify_subtype"): {
        "address": "Check Box3",
        "name": "Check Box5"},
    ("NP_CLKRA-3", "clerk_change.bc_authorization"): {
        "board_of_directors": "Check Box12",
        "shareholders": "Check Box13"},
    ("CORP_CLKRA-3", "clerk_change.modify_subtype"): {
        "address": "Check Box3",
        "name": "Check Box5"},
    ("NP_MLC-3_0", "clerk_change.change_type"): {
        "address": "Check Box1",
        "clerk_and_address": "Check Box3",
        "clerk": "Check Box2",
        "clerk_name": "Check Box4"},
    ("NP_MNP-6", "entity.nonprofit_type"): {
        "public_benefit": "Check Box2",
        "mutual_benefit": "Check Box3"},
    ("NP_MNP-981A", "entity.nonprofit_type"): {
        "public_benefit": "Check Box4",
        "mutual_benefit": "Check Box5"},
    ("NP_MNP-981A", "entity.management_structure"): {
        "directors": "Check Box6",
        "members": "Check Box7"},
    ("NP_MNPCA-10", "merger.parties[0].vote_method"): {
        "majority_member_vote": "Check Box1",
        "supermajority_member_vote": "Check Box2",
        "written_consent_of_members": "Check Box3",
        "board_of_directors_majority_vote": "Check Box4"},
    ("NP_MNPCA-10", "merger.parties[1].vote_method"): {
        "majority_member_vote": "Check Box5",
        "supermajority_member_vote": "Check Box6",
        "written_consent_of_members": "Check Box7",
        "board_of_directors_majority_vote": "Check Box8"},
    ("NP_MNPCA-10A", "consolidation.parties[0].vote_method"): {
        "majority_member_vote": "Check Box1",
        "supermajority_member_vote": "Check Box2",
        "written_consent_of_members": "Check Box3",
        "board_of_directors_majority_vote": "Check Box5"},
    ("NP_MNPCA-10A", "consolidation.parties[1].vote_method"): {
        "majority_member_vote": "Check Box6",
        "supermajority_member_vote": "Check Box7",
        "written_consent_of_members": "Check Box8",
        "board_of_directors_majority_vote": "Check Box9"},
    ("NP_MNPCA-10C", "merger.surviving_corp.benefit_type"): {
        "public_benefit": "Check Box4",
        "mutual_benefit": "Check Box5"},
    ("NP_MNPCA-10C", "merger.domestic_corp.vote_method"): {
        "majority_member_vote": "Check Box8",
        "supermajority_member_vote": "Check Box9",
        "written_consent_of_members": "Check Box10",
        "board_of_directors_majority_vote": "Check Box11"},
    ("NP_MNPCA-10E", "consolidation.parties[0].adoption_method"): {
        "majority_member_vote": "Check Box8",
        "supermajority_member_vote": "Check Box9",
        "written_consent_of_members": "Check Box11",
        "board_of_directors_majority_vote": "Check Box13"},
    ("NP_MNPCA-11", "dissolution.consent_class"): {
        "members": "Check Box16__p0",
        "directors_when_no_voting_members": "Check Box17"},
    ("NP_MNPCA-11A", "dissolution.consent_class"): {
        "members": "Check Box29",
        "directors_when_no_voting_members": "Check Box30"},
    ("NP_MNPCA-11C", "revocation.consent_class"): {
        "members": "Check Box6",
        "directors_when_no_voting_members": "Check Box5"},
    ("NP_MNPCA-14A", "resumption.adopting_body"): {
        "members": "Check Box4",
        "directors": "Check Box5"},
    ("NP_MNPCA-14A", "resumption.method"): {
        "meeting": "Check Box6",
        "written_consent": "Check Box7"},
    ("NP_MNPCA-14A", "resumption.voting_body"): {
        "members": "Check Box8",
        "directors": "Check Box9"},
    ("NP_MNPCA-14A", "entity.nonprofit_type"): {
        "public_benefit": "Check Box10",
        "mutual_benefit": "Check Box11"},
    ("NP_MNPCA-6-1", "entity.nonprofit_type"): {
        "public_benefit": "Check Box10",
        "mutual_benefit": "Check Box11"},
    ("NP_MNPCA-9", "entity.nonprofit_type"): {
        "public_benefit": "Check Box4",
        "mutual_benefit": "Check Box5"},
    ("NP_MNPCA-6A_0", "restatement.adoption_method"): {
        "members_majority_at_meeting": "Check Box4",
        "members_supermajority_at_meeting": "Check Box5",
        "members_written_consent": "Check Box6",
        "board_majority": "Check Box8"},
}

#: (form, key, widget) for single yes/this-applies boxes retyped to boolean.
BOOLEANS = [
    ("CORP_MBCA-12A", "filing.fict4_accompanies", "Check Box1"),
    ("LLP_MLLP-12", "filing.fict4_accompanies", "Check Box23"),
    ("LLP_MLLP-12-1", "filing.fict4_accompanies", "Check Box19"),
    ("LLP_MLLP-12A", "filing.fict4_accompanies", "Check Box4"),
    ("LP_MLPA-12", "filing.fict4_accompanies", "Check Box4"),
    ("LP_MLPA-12-1", "filing.fict4_accompanies", "Check Box23"),
    ("NP_MNPCA-12-1", "filing.fict4_accompanies", "Check Box1"),
    ("LLC_MLLC-10", "merger.additional_parties_attached", "Check Box10"),
    ("LP_MLPA-10", "merger.additional_parties_attached", "Check Box19"),
    ("LP_MLPA-12", "general_partner.additional_attached", "Check Box31"),
    ("LP_MLPA-12-1", "general_partner.additional_attached", "Check Box28"),
    ("LP_MLPA-6-1", "general_partner.additional_attached", "Check Box26"),
    ("LP_MLPA-6A", "general_partner.additional_attached", "Check Box18"),
    ("MARK_mark2", "mark.additional_pages_attached", "Check Box9"),
    ("NP_MNPCA-6-1", "entity.no_political_activities_clause", "Check Box16"),
    ("NP_MNPCA-6A_0", "filing.expedited_service.hold_for_pickup", "Check Box20"),
    ("NP_MNPCA-6A_0", "filing.expedited_service.expedite_24h", "Check Box21"),
    ("NP_MNPCA-6A_0", "filing.expedited_service.immediate", "Check Box22"),
]


def _case_for(key, value):
    case = {}
    node = case
    parts = key.split(".")
    for i, part in enumerate(parts):
        m = re.match(r"(\w+)\[(\d+)\]$", part)
        if m:
            arr = node.setdefault(m.group(1), [])
            while len(arr) <= int(m.group(2)):
                arr.append({})
            node = arr[int(m.group(2))]
        elif i == len(parts) - 1:
            node[part] = value
        else:
            node = node.setdefault(part, {})
    return case


def _binding(fid, key):
    mapping = json.loads((FORMS / fid / "mapping.json").read_text())
    hits = [(anchor, spec) for anchor, spec in mapping["map"].items()
            if isinstance(spec, dict) and spec.get("key") == key]
    assert len(hits) == 1, f"{fid}: expected exactly one {key} binding"
    return hits[0]


def _schema_leaf(fid, key):
    node = json.loads((FORMS / fid / "schema.json").read_text())
    parts = re.sub(r"\[\d+\]", "", key).split(".")
    for i, part in enumerate(parts):
        props = node.get("properties")
        if props is None and node.get("type") == "array":
            node = node["items"]
            props = node.get("properties")
        node = props[part]
        if node.get("type") == "array" and i < len(parts) - 1:
            node = node["items"]
    return node


@pytest.mark.parametrize("fid,key", sorted(ENUM_SELECTS))
def test_enum_binding_shape(fid, key):
    anchor, spec = _binding(fid, key)
    options = ENUM_SELECTS[(fid, key)]
    assert spec.get("field_type") == "enum_select"
    assert spec.get("options") == options
    assert anchor == next(iter(options.values()))
    assert "widgets" not in spec  # the fan-out list is gone


@pytest.mark.parametrize("fid,key", sorted(ENUM_SELECTS))
def test_schema_pins_the_enum(fid, key):
    leaf = _schema_leaf(fid, key)
    assert leaf.get("enum") == list(ENUM_SELECTS[(fid, key)])


@pytest.mark.parametrize("fid,key", sorted(ENUM_SELECTS))
def test_resolution_selects_exactly_one(fid, key):
    options = ENUM_SELECTS[(fid, key)]
    for value, chosen in options.items():
        report = {}
        plan = fill.resolve_fill(fid, _case_for(key, value), str(FORMS),
                                 report=report)
        assert report["dropped_enums"] == []
        assert plan["field_data"][chosen] == "Yes"
        for sibling in options.values():
            if sibling != chosen:
                assert plan["field_data"][sibling] == ""


@pytest.mark.parametrize("fid,key", sorted(ENUM_SELECTS))
def test_unmapped_value_is_reported_not_written(fid, key):
    options = ENUM_SELECTS[(fid, key)]
    report = {}
    plan = fill.resolve_fill(fid, _case_for(key, "bogus_value"), str(FORMS),
                             report=report)
    assert report["dropped_enums"] == [
        {"key": key, "value": "bogus_value", "allowed": sorted(options)}]
    for widget in options.values():
        assert widget not in plan["field_data"]


@pytest.mark.parametrize("fid,key,widget", BOOLEANS)
def test_boolean_binding(fid, key, widget):
    anchor, spec = _binding(fid, key)
    assert anchor == widget
    assert spec.get("field_type") == "checkbox"
    assert "widgets" not in spec
    assert _schema_leaf(fid, key).get("type") == "boolean"
    plan = fill.resolve_fill(fid, _case_for(key, True), str(FORMS))
    assert plan["field_data"][widget] == "Yes"
    plan = fill.resolve_fill(fid, _case_for(key, False), str(FORMS))
    assert widget not in plan["field_data"]  # never an explicit uncheck


def test_no_text_binding_touches_button_widgets():
    """The smell class cannot regress: no text-typed binding on /Btn widgets.

    This is the sweep's authoritative scan, kept as a test. ``enum_select`` /
    ``radio`` / ``checkbox`` / ``enum_text_select`` bindings are the only
    legitimate ways to put a fact key onto a button field.
    """
    from pypdf import PdfReader

    offenders = []
    for d in sorted(FORMS.iterdir()):
        mp = d / "mapping.json"
        pdfs = list(d.glob("*.pdf"))
        if not mp.exists() or not pdfs:
            continue
        fields = PdfReader(str(pdfs[0])).get_fields() or {}
        btn = {n for n, f in fields.items() if f.get("/FT") == "/Btn"}
        mapping = json.loads(mp.read_text())
        for anchor, spec in (mapping.get("map") or {}).items():
            if not isinstance(spec, dict):
                continue
            if spec.get("field_type", "text") != "text":
                continue
            widgets = spec.get("widgets") or [anchor]
            hit = [w for w in widgets if w.split("__p")[0] in btn]
            if hit:
                offenders.append(f"{d.name}: {spec.get('key')} -> {hit}")
    assert not offenders, "text-typed bindings on /Btn widgets:\n" + \
        "\n".join(offenders)
