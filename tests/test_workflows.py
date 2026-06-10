"""catalog/workflows.json integrity: shape, references, and honesty flags."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _workflows():
    return json.loads(
        (ROOT / "catalog" / "workflows.json").read_text())["workflows"]


def _known_form_ids():
    index = json.loads((ROOT / "catalog" / "forms_index.json").read_text())
    return {f["form_id"] for f in index["forms"]}


def test_workflow_ids_unique_and_slug_like():
    ids = [w["id"] for w in _workflows()]
    assert len(ids) == len(set(ids))
    assert all(i and i.replace("_", "").isalnum() and i == i.lower()
               for i in ids)


def test_every_step_form_id_exists_in_catalog():
    known = _known_form_ids()
    for wf in _workflows():
        for step in wf["steps"]:
            assert step["form_id"] in known, (
                f"{wf['id']}: unknown form_id {step['form_id']!r}")


def test_workflow_shape():
    for wf in _workflows():
        assert wf.get("title") and wf.get("when"), wf["id"]
        assert wf["steps"], f"{wf['id']}: empty steps"
        for step in wf["steps"]:
            assert isinstance(step["required"], bool), wf["id"]
            assert step.get("note"), (
                f"{wf['id']}/{step['form_id']}: every step needs a note "
                "saying what is printed on the form or what was inferred")
            if "inferred" in step:
                assert step["inferred"] is True, (
                    f"{wf['id']}/{step['form_id']}: 'inferred' is only "
                    "present (and true) when the link is not printed")


def test_each_workflow_has_a_required_anchor_step():
    for wf in _workflows():
        assert any(s["required"] for s in wf["steps"]), wf["id"]


def test_inferred_steps_are_flagged_not_silent():
    # Lifecycle groupings (name reservation, assumed name) and unprinted
    # form-id mappings must carry inferred=true; spot-check known ones.
    by_id = {w["id"]: w for w in _workflows()}
    res = next(s for s in by_id["corp_formation"]["steps"]
               if s["form_id"] == "CORP_MBCA-1")
    assert res.get("inferred") is True
    amend = next(s for s in by_id["indistinguishable_name_corp"]["steps"]
                 if s["form_id"] == "CORP_MBCA-9")
    assert amend.get("inferred") is True


def test_printed_companion_links_present():
    # The load-bearing printed accompaniments must stay in the data.
    by_id = {w["id"]: w for w in _workflows()}

    def step_ids(wf_id):
        return {s["form_id"] for s in by_id[wf_id]["steps"]}

    assert "CORP_MBCA-6-1" in step_ids("corp_restated_articles")
    assert "NP_MNPCA-6-1" in step_ids("np_restated_articles")
    assert "CORP_MBCA-6-1" in step_ids("corp_domestication")
    assert "NP_MNPCA-6-1" in step_ids("corp_nonprofit_conversion")
    assert "CORP_MBCA-6-1" in step_ids("corp_entity_conversion_to_corp")
    assert {"LLC_MLLC-6", "LP_MLPA-6-1"} <= step_ids(
        "corp_entity_conversion_from_corp")
    assert {"LP_MLPA-6-1", "LLC_MLLC-6", "CORP_MBCA-6-1"} <= step_ids(
        "gp_conversion_of_partnership")
    assert "CORP_FICT-4" in step_ids("corp_foreign_qualification")
