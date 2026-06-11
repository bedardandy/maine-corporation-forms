"""Cross-form canonical-key lint.

The data model gets its value from keys meaning the same thing on every form.
A key whose leaf is used by exactly ONE form while a near-identical sibling
leaf (same parent path) is used by many is almost always drift — e.g.
``filing.signer.printed_name_and_title`` on one form vs the 69-form
``filing.signer.printed_name_and_capacity``. Known-intentional variants are
allowlisted below; add to the list only after checking the form's printed
labels.
"""
import collections
import difflib
import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.mapping import entries as mapping_entries  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "forms"

# (parent_path, lone_leaf, common_leaf) triples reviewed and kept on purpose.
ALLOWED_LONERS = {
    # LLC_MLLC-12A: a different cover question than the fict4 family.
    ("filing", "fict_form_accompanies", "fict4_accompanies"),
    # CORP_MBCA-12A asks for the jurisdiction *as on record*, not a free name.
    ("entity", "home_jurisdiction_on_record", "home_jurisdiction_name"),
    # NP_MNPCA-12 genuinely has a two-line physical address widget pair.
    ("entity.principal_office", "physical_address_line1", "physical_address"),
    ("entity.principal_office", "physical_address_line2", "physical_address"),
}

_MIN_COMMON_FORMS = 10
_SIMILARITY = 0.8


def _canonical_keys():
    """Yield (form_id, canonical_key) for every mapping entry."""
    for d in sorted(FORMS.iterdir()):
        mp = d / "mapping.json"
        if not d.is_dir() or not mp.exists():
            continue
        mapping = json.loads(mp.read_text())
        for key, spec in mapping_entries(mapping).items():
            ckey = spec.get("canonical_key", key) if isinstance(spec, dict) else key
            yield mapping["form_id"], re.sub(r"\[\d+\]", "[]", ckey)


def test_no_one_form_near_miss_keys():
    leaf_forms = collections.defaultdict(set)
    for fid, ckey in _canonical_keys():
        parent, _, leaf = ckey.rpartition(".")
        leaf_forms[(parent, leaf)].add(fid)

    by_parent = collections.defaultdict(dict)
    for (parent, leaf), fids in leaf_forms.items():
        by_parent[parent][leaf] = fids

    findings = []
    for parent, leaves in by_parent.items():
        for leaf, fids in leaves.items():
            if len(fids) != 1:
                continue
            for other, other_fids in leaves.items():
                if other == leaf or len(other_fids) < _MIN_COMMON_FORMS:
                    continue
                close = difflib.SequenceMatcher(None, leaf, other).ratio()
                if close < _SIMILARITY:
                    continue
                if (parent, leaf, other) in ALLOWED_LONERS:
                    continue
                findings.append(
                    f"{sorted(fids)[0]}: {parent}.{leaf} is used by no other "
                    f"form but {parent}.{other} is used by "
                    f"{len(other_fids)} — likely key drift")
    assert not findings, "\n".join(findings)
