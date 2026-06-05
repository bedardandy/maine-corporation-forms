"""Who may sign, and how, for each Maine SoS business-entity form.

Maine generally requires an *original wet-ink signature* on paper business
filings, and statute restricts *who* may sign by entity type and filing kind.
This module encodes that as data so it can be validated deterministically rather
than left to a language model:

* ``signature_mode`` -- ``wet_ink`` (print and sign by hand; the default for
  these filings) or ``e_sign_ok`` (an electronic signature is acceptable).
* ``allowed_signer_capacities`` -- the capacities in which a person may sign
  this form (e.g. ``incorporator``, ``officer``, ``authorized person``,
  ``general partner``, ``partner``, ``registered agent``).

The capacity scaffold below is grounded in the Maine entity statutes, but the
*authoritative* statement of who signs is printed in each form's own signature
block. Treat these defaults as a verified starting point; a per-form
``forms/<ID>/signer_rules.json`` may override them where a form's printed block
says otherwise.

Nothing here ever types a signature: the signature *line* stays blank for the
pen. Only the signer's printed name, title/capacity, and date go into their
designated text fields.
"""

from __future__ import annotations

import json
from pathlib import Path

# Entity class -> default signer rules, keyed by the form-id prefix (which is
# the reliable discriminator: CORP_/NP_/LLC_/LP_/LLP_/GP_/MARK_).
_DEFAULTS = {
    "CORP": {
        "entity": "Business Corporation (13-C M.R.S.)",
        "formation": ["incorporator"],
        "other": ["officer", "incorporator", "director"],
    },
    "NP": {
        "entity": "Nonprofit Corporation (13-B M.R.S.)",
        "formation": ["incorporator"],
        "other": ["officer", "director", "incorporator"],
    },
    "LLC": {
        "entity": "Limited Liability Company (31 M.R.S.)",
        "formation": ["authorized person", "member", "manager"],
        "other": ["authorized person", "member", "manager"],
    },
    "LP": {
        "entity": "Limited Partnership (31 M.R.S.)",
        # A certificate of LP is signed by all general partners; amendments by a
        # general partner.
        "formation": ["general partner"],
        "other": ["general partner"],
    },
    "LLP": {
        "entity": "Limited Liability Partnership (31 M.R.S.)",
        "formation": ["partner", "authorized partner"],
        "other": ["partner", "authorized partner"],
    },
    "GP": {
        "entity": "General Partnership (31 M.R.S.)",
        "formation": ["partner"],
        "other": ["partner"],
    },
    "MARK": {
        "entity": "Trademark / Service Mark (10 M.R.S.)",
        "formation": ["applicant", "officer", "authorized person"],
        "other": ["applicant", "officer", "authorized person"],
    },
}

# Forms whose primary act is to designate or change a registered agent also
# carry an agent-acceptance signed by the registered agent itself.
_AGENT_ACCEPTANCE_HINT = ("agent", "registered")

# Capacity synonyms -> canonical capacity, so validation is robust to phrasing.
_CAPACITY_SYNONYMS = {
    "inc": "incorporator",
    "incorporator": "incorporator",
    "officer": "officer",
    "president": "officer",
    "vice president": "officer",
    "vp": "officer",
    "secretary": "officer",
    "treasurer": "officer",
    "ceo": "officer",
    "cfo": "officer",
    "clerk": "officer",
    "director": "director",
    "member": "member",
    "manager": "manager",
    "authorized person": "authorized person",
    "authorized representative": "authorized person",
    "authorized rep": "authorized person",
    "general partner": "general partner",
    "gp": "general partner",
    "partner": "partner",
    "authorized partner": "authorized partner",
    "registered agent": "registered agent",
    "agent": "registered agent",
    "applicant": "applicant",
    "owner": "applicant",
}


def entity_class(form_id: str) -> str:
    prefix = form_id.split("_", 1)[0].upper()
    return prefix if prefix in _DEFAULTS else "CORP"


def _forms_root(forms_root: str) -> Path:
    root = Path(forms_root)
    if root.is_absolute():
        return root
    here = Path(__file__).resolve().parent.parent
    return here / forms_root


def _read_form_meta(form_id: str, forms_root: str) -> dict:
    root = _forms_root(forms_root)
    path = root / form_id / "form.yaml"
    try:
        import yaml

        return yaml.safe_load(path.read_text()) or {}
    except Exception:
        return {}


def normalize_capacity(value: str) -> str:
    """Canonicalize a free-text capacity to one of the known capacities."""
    v = (value or "").strip().lower()
    if v.startswith("the "):
        v = v[4:].strip()
    if v in _CAPACITY_SYNONYMS:
        return _CAPACITY_SYNONYMS[v]
    # Substring match (e.g. "sole incorporator", "managing member").
    for token, canon in _CAPACITY_SYNONYMS.items():
        if token in v:
            return canon
    return v


def rules_for(form_id: str, forms_root: str = "forms") -> dict:
    """Return the signer rules for one form (override file wins over defaults)."""
    root = _forms_root(forms_root)
    override = root / form_id / "signer_rules.json"
    if override.exists():
        try:
            data = json.loads(override.read_text())
            data.setdefault("source", "override")
            return data
        except Exception:
            pass

    meta = _read_form_meta(form_id, forms_root)
    cls = entity_class(form_id)
    spec = _DEFAULTS[cls]
    category = (meta.get("category") or "").lower()
    title_l = (meta.get("title") or "").lower()
    # ``category`` is absent on many form.yaml files, so also detect a formation
    # filing from its title (Articles of Incorporation / Organization,
    # Certificate of Formation / Limited Partnership, ...).
    _FORMATION_TITLES = (
        "articles of incorporation",
        "articles of organization",
        "certificate of formation",
        "certificate of limited partnership",
        "registration",
        "qualification",
        "statement of qualification",
    )
    is_formation = category in {"formation", "registration", "qualification"} or any(
        t in title_l for t in _FORMATION_TITLES
    )
    allowed = list(spec["formation"] if is_formation else spec["other"])

    fid_l = form_id.lower()
    title_l = (meta.get("title") or "").lower()
    if any(h in fid_l or h in title_l for h in _AGENT_ACCEPTANCE_HINT):
        if "registered agent" not in allowed:
            allowed.append("registered agent")

    return {
        "form_id": form_id,
        "entity_class": cls,
        "entity": spec["entity"],
        "category": meta.get("category"),
        "signature_mode": "wet_ink",
        "allowed_signer_capacities": allowed,
        "note": (
            "Maine generally requires an original wet-ink signature on paper "
            "filings. Verify the form's printed signature block for the "
            "authoritative signer."
        ),
        "source": "default",
    }


def validate(form_id: str, case: dict, forms_root: str = "forms") -> list:
    """Check a case's declared signer capacity against the form's rules.

    Looks for ``case['signature']['capacity']`` (and any
    ``case['signatures'][*]['capacity']``). Returns a list of issue dicts;
    empty means no signer problems were found. Absence of a signature block is
    reported as a ``warning`` (not a hard error) so partial drafts still pass.
    """
    rules = rules_for(form_id, forms_root)
    allowed = {c.lower() for c in rules["allowed_signer_capacities"]}
    issues: list = []

    blocks = []
    sig = (case or {}).get("signature")
    if isinstance(sig, dict):
        blocks.append(sig)
    multi = (case or {}).get("signatures")
    if isinstance(multi, list):
        blocks.extend(b for b in multi if isinstance(b, dict))

    if not blocks:
        issues.append(
            {
                "severity": "warning",
                "code": "no-signature-block",
                "message": "No signature block in case data; signer not validated.",
            }
        )
        return issues

    for i, b in enumerate(blocks):
        cap_raw = b.get("capacity") or b.get("title") or ""
        cap = normalize_capacity(cap_raw)
        if not cap:
            issues.append(
                {
                    "severity": "required",
                    "code": "missing-capacity",
                    "index": i,
                    "message": "Signer capacity is missing.",
                }
            )
            continue
        if cap not in allowed:
            issues.append(
                {
                    "severity": "required",
                    "code": "capacity-not-allowed",
                    "index": i,
                    "message": (
                        f"Signer capacity {cap_raw!r} (→ {cap!r}) is not "
                        f"permitted for {form_id}; allowed: {sorted(allowed)}."
                    ),
                }
            )
    return issues


def build_catalog(forms_root: str = "forms", out_path=None) -> dict:
    """Build a static {form_id: rules} catalog for all forms."""
    root = _forms_root(forms_root)
    catalog: dict = {}
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        fid = d.name
        if not (d / "form.yaml").exists():
            continue
        catalog[fid] = rules_for(fid, forms_root)
    if out_path:
        Path(out_path).write_text(json.dumps(catalog, indent=2, sort_keys=True))
    return catalog


def _main(argv) -> int:
    if argv and argv[0] == "build":
        here = Path(__file__).resolve().parent.parent
        out = here / "catalog" / "signer_rules.json"
        cat = build_catalog("forms", str(out))
        print(f"wrote {out} ({len(cat)} forms)", flush=True)
        return 0
    if len(argv) >= 1:
        print(json.dumps(rules_for(argv[0]), indent=2), flush=True)
        return 0
    print("usage: python3 -m tools.signer_rules <FORM_ID> | build", flush=True)
    return 2


if __name__ == "__main__":
    import sys

    raise SystemExit(_main(sys.argv[1:]))
