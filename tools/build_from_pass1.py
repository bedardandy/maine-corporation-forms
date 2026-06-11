#!/usr/bin/env python3
"""Deterministic generator for maine-corporation-forms.

Reads blank Maine Secretary of State AcroForm PDFs plus the corresponding
pass-1 field-mapping JSON files and emits, for each form:

    forms/<FORM_ID>/
        <FORM_ID>.pdf      copied blank form
        form.yaml          metadata
        mapping.json       canonical_key -> widget spec
        schema.json        JSON Schema (draft 2020-12) for fill data
        fields.csv         flat field inventory
        rubric.yaml        validation checks
        README.md          human-readable summary
        SKILL.md           agent fill guidance

It also writes the catalog (forms_index.json, pdf_manifest.json,
by_entity.json) and a coverage / mismatch report to docs/STATUS.md.

The script validates every mapped widget against the real AcroForm field
names in each PDF and records mismatches. It is re-runnable and idempotent:
each run regenerates the artifacts from the source inputs.

Inputs are configured via --pdf-dir and --pass1-dir (or the SOS_PDF_DIR /
SOS_PASS1_DIR environment variables). No paths are hard-coded.

Dependencies: standard library + pypdf.
"""
import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import pypdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine import mapping as mapping_mod  # noqa: E402

# ---------------------------------------------------------------------------
# Hand-maintained forms: these have been reconciled by hand after pass-1 and
# must NOT be clobbered by a regen. Skipped by default; pass --force to
# override. The authoritative list lives in tools/HAND_MAINTAINED.txt; this
# frozenset is only the fallback used when that file is absent.
# ---------------------------------------------------------------------------
HAND_MAINTAINED = frozenset({
    "CORP_MBCA-6",
    "CORP_MBCA-6-1",
    "CORP_MBCA-10",
    "NP_MNP-9",
    "NP_MNPCA-11",
    "LP_MLPA-9",
})


def load_hand_maintained():
    """Read the hand-maintained id list from the sidecar file, else fall back."""
    path = Path(__file__).resolve().parent / "HAND_MAINTAINED.txt"
    if not path.exists():
        return set(HAND_MAINTAINED)
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ids.add(line)
    return ids or set(HAND_MAINTAINED)

# ---------------------------------------------------------------------------
# Entity-type taxonomy: maps the form-id prefix to a human label + statute.
# ---------------------------------------------------------------------------
ENTITY_TYPES = {
    "CORP": ("Business Corporation", "Maine Business Corporation Act (13-C M.R.S.)"),
    "NP": ("Nonprofit Corporation", "Maine Nonprofit Corporation Act (13-B M.R.S.)"),
    "LLC": ("Limited Liability Company", "Maine Limited Liability Company Act (31 M.R.S. ch. 21)"),
    "LP": ("Limited Partnership", "Maine Revised Uniform Limited Partnership Act (31 M.R.S.)"),
    "LLP": ("Limited Liability Partnership", "Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)"),
    "GP": ("General Partnership", "Maine Uniform Partnership Act (31 M.R.S.)"),
    "MARK": ("Trademark / Service Mark", "Maine Trademark Act (10 M.R.S. ch. 301-A)"),
}

# A handful of categories observed in the pass-1 data map cleanly to a prefix;
# the prefix is authoritative, this is only a fallback label.
CATEGORY_LABEL = {
    "business_corporation": "Business Corporation",
    "nonprofit": "Nonprofit Corporation",
    "limited_liability_company": "Limited Liability Company",
    "limited_partnership": "Limited Partnership",
    "limited_liability_partnership": "Limited Liability Partnership",
    "general_partnership": "General Partnership",
    "trademark": "Trademark / Service Mark",
}


def prefix_of(form_id):
    return form_id.split("_", 1)[0]


def entity_meta(form_id):
    pre = prefix_of(form_id)
    if pre in ENTITY_TYPES:
        return ENTITY_TYPES[pre]
    return ("Other", "Maine Secretary of State filing")


def bare_code(form_id):
    """CORP_MBCA-6 -> MBCA-6 ; LLC_MLLC-1 -> MLLC-1."""
    parts = form_id.split("_", 1)
    return parts[1] if len(parts) == 2 else form_id


# ---------------------------------------------------------------------------
# Type inference for schema.json
# ---------------------------------------------------------------------------
def parse_enum(description):
    """Extract enum values from a description containing 'Enum: a, b, c'."""
    if not description:
        return None
    marker = "Enum:"
    idx = description.find(marker)
    if idx == -1:
        return None
    tail = description[idx + len(marker):].strip()
    # take up to the first sentence break
    for stop in (". ", ";"):
        if stop in tail:
            tail = tail.split(stop, 1)[0]
    tail = tail.rstrip(". ")
    # Enum values are written as "'a' | 'b' | 'c'" or "'a', 'b', 'c'".
    if "|" in tail:
        parts = tail.split("|")
    else:
        parts = tail.split(",")
    values = []
    for p in parts:
        v = p.strip()
        # drop any trailing parenthetical gloss first, e.g. "'immediate' (same day)"
        if " (" in v:
            v = v.split(" (", 1)[0].strip()
        # then strip surrounding quotes
        v = v.strip("'\"").strip()
        if v:
            values.append(v)
    return values or None


def infer_type(key, description):
    """Return (json_type, enum_or_None) for a canonical key."""
    last = key.split(".")[-1]
    desc = description or ""
    enum = parse_enum(desc)
    if enum:
        return "string", enum
    # booleans: is_/has_ prefixes, elect-in style suffixes, or explicit note
    if (
        last.startswith(("is_", "has_"))
        or last.endswith(("_elected", "_limited", "_present", "_required"))
        or "Boolean" in desc
        or "boolean" in desc
    ):
        return "boolean", None
    # integers: counts and share quantities (but not phone numbers / public
    # numbers). Token-bounded so "count" never matches inside "county" — a
    # bare substring test used to type county fields as integers.
    if (
        re.search(r"(?:^|_)count(?:$|_)", last)
        or "shares" in last
        or (re.search(r"(?:^|_)number(?:$|_)", last)
            and "phone" not in last and "public" not in last
            and "cra" not in last)
    ):
        return "integer", None
    return "string", None


# ---------------------------------------------------------------------------
# Nested schema construction from dotted keys
# ---------------------------------------------------------------------------
_ARRAY_SEG_RE = re.compile(r"^(\w+)\[(?:\d+|N|n|\*)?\]$")
_BRACE_GROUP_RE = re.compile(r"^(\w*)\{([\w\s,]+)\}(\w*)$")


def expand_key_notation(dotted_key):
    """Expand pass-1 shorthand into one or more plain dotted keys.

    Pass-1 ``proposed_key`` values use index and brace notation —
    ``parties[0].name``, ``class_changes[N]``, ``line{1,2}``,
    ``address.{street,city}``. Brace groups multiply into one key per
    member; index segments are normalized to ``name[]`` so
    :func:`set_nested_property` builds an array (every index shares one
    item schema). Returning these as *literal property names* was the bug
    that produced schema properties like ``"class_changes[0]"``.
    """
    keys = [""]
    for raw in dotted_key.split("."):
        m = _BRACE_GROUP_RE.match(raw)
        if m:
            prefix, parts, suffix = m.group(1), m.group(2), m.group(3)
            variants = [f"{prefix}{p.strip()}{suffix}"
                        for p in parts.split(",") if p.strip()]
        else:
            m = _ARRAY_SEG_RE.match(raw)
            variants = [f"{m.group(1)}[]"] if m else [raw]
        keys = [f"{k}.{v}" if k else v for k in keys for v in variants]
    return keys


def set_nested_property(root_props, dotted_key, leaf_schema):
    """Insert leaf_schema at the dotted path inside a JSON-Schema properties tree.

    List segments (key[]) become array-of-object containers.
    """
    parts = dotted_key.split(".")
    props = root_props
    for i, raw in enumerate(parts):
        is_last = i == len(parts) - 1
        is_array = raw.endswith("[]")
        name = raw[:-2] if is_array else raw
        if is_last:
            if is_array:
                node = props.setdefault(name, {"type": "array", "items": {"type": "object", "properties": {}}})
                # a bare array leaf: keep object items
                _ = node
            else:
                props[name] = leaf_schema
            return
        # intermediate node
        if is_array:
            node = props.setdefault(name, {"type": "array", "items": {"type": "object", "properties": {}}})
            props = node["items"]["properties"]
        else:
            node = props.setdefault(name, {"type": "object", "properties": {}})
            if node.get("type") != "object":
                # was previously a leaf; promote to object
                node.clear()
                node.update({"type": "object", "properties": {}})
            props = node["properties"]


def build_schema(form_id, schema_gaps, mapping_keys, rubric_checks):
    """Build a draft-2020-12 schema from schema_gaps (falling back to mapping keys)."""
    properties = {}
    described = {}

    # Index descriptions from schema_gaps
    gap_index = {}
    for g in schema_gaps:
        k = g.get("proposed_key")
        if k:
            gap_index[k] = g.get("description", "")

    # Use the union of schema-gap keys and mapping keys so every fillable key
    # appears in the schema.
    all_keys = list(dict.fromkeys(list(gap_index.keys()) + list(mapping_keys)))

    for key in all_keys:
        desc = gap_index.get(key, "")
        # pass-1 keys may carry index/brace shorthand ("parties[0].name",
        # "line{1,2}") — expand before insertion so notation never leaks
        # into literal property names.
        for expanded in expand_key_notation(key):
            jtype, enum = infer_type(expanded, desc)
            leaf = {"type": jtype}
            if desc:
                leaf["description"] = desc
            if enum:
                leaf["enum"] = enum
            set_nested_property(properties, expanded, leaf)
            described[expanded] = leaf

    # Required: only keys whose rubric check is severity=required AND that is a
    # single-key presence check (keep required minimal and safe).
    required_top = []
    for chk in rubric_checks:
        if chk.get("severity") == "required":
            deps = chk.get("depends_on_keys") or []
            if len(deps) == 1:
                top = deps[0].split(".")[0].replace("[]", "")
                if top not in required_top and top in properties:
                    required_top.append(top)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://maine-corporation-forms/schemas/{form_id}.json",
        "title": f"{form_id} fill data",
        "type": "object",
        "properties": properties,
        "required": sorted(required_top),
    }
    return schema


# ---------------------------------------------------------------------------
# mapping.json construction
# ---------------------------------------------------------------------------
def build_mapping(form_id, field_mappings):
    """canonical_key -> {widget_id (str|list), field_type, page, confidence, label}.

    When several widgets share one canonical key, widget_id becomes a list.
    """
    grouped = {}
    order = []
    for m in field_mappings:
        key = m.get("proposed_canonical_key")
        wid = m.get("field_id")
        if not key or not wid:
            continue
        if key not in grouped:
            grouped[key] = {
                "widget_ids": [],
                "field_type": None,
                "page": m.get("page"),
                "confidence": m.get("confidence", "low"),
                "label": m.get("nearby_label_text", ""),
            }
            order.append(key)
        g = grouped[key]
        if wid not in g["widget_ids"]:
            g["widget_ids"].append(wid)
        # field type heuristic from key/widget name
        ft = infer_field_type(key, wid, m.get("nearby_label_text", ""))
        if g["field_type"] is None:
            g["field_type"] = ft
        # keep the highest confidence seen, but downgrade to lowest? Use the
        # min so a shared key reflects its weakest evidence.
        g["confidence"] = lower_confidence(g["confidence"], m.get("confidence", "low"))

    fields = {}
    for key in order:
        g = grouped[key]
        wids = g["widget_ids"]
        fields[key] = {
            "widget_id": wids[0] if len(wids) == 1 else wids,
            "field_type": g["field_type"],
            "page": g["page"],
            "confidence": g["confidence"],
            "label": g["label"],
        }
    return {"form_id": form_id, "fields": fields}


CONF_RANK = {"high": 3, "medium": 2, "low": 1}


def lower_confidence(a, b):
    ra, rb = CONF_RANK.get(a, 1), CONF_RANK.get(b, 1)
    return a if ra <= rb else b


def infer_field_type(key, widget_id, label):
    if not key:
        return "text"
    last = key.split(".")[-1]
    wid = (widget_id or "").lower()
    lab = (label or "").lower()
    if (
        last.startswith(("is_", "has_"))
        or last.endswith(("_elected", "_limited", "_present", "_required"))
        or "checkbox" in wid
        or "check" in lab
    ):
        return "checkbox"
    return "text"


# ---------------------------------------------------------------------------
# PDF inspection
# ---------------------------------------------------------------------------
def pdf_info(pdf_path):
    """Return (num_pages, set_of_field_names, has_acroform)."""
    reader = pypdf.PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    field_names = set()
    has_acro = False
    try:
        fields = reader.get_fields()
    except Exception:
        fields = None
    if fields:
        has_acro = True
        field_names = set(fields.keys())
    return num_pages, field_names, has_acro


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# YAML emit (tiny, dependency-free, sufficient for our flat/simple structures)
# ---------------------------------------------------------------------------
def yaml_scalar(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if s == "" or any(c in s for c in ":#{}[],&*!|>'\"%@`") or s.strip() != s:
        return json.dumps(s, ensure_ascii=False)
    return s


def emit_form_yaml(meta):
    lines = []
    for k in ("form_id", "code", "title", "entity_type", "statute",
              "num_pages", "num_fields", "mapped_fields", "source", "revision",
              "jurisdiction", "language"):
        lines.append(f"{k}: {yaml_scalar(meta.get(k))}")
    return "\n".join(lines) + "\n"


def emit_rubric_yaml(checks):
    if not checks:
        return "checks: []\n"
    lines = ["checks:"]
    for c in checks:
        lines.append(f"  - id: {yaml_scalar(c.get('id'))}")
        lines.append(f"    description: {yaml_scalar(c.get('description'))}")
        deps = c.get("depends_on_keys") or []
        if deps:
            lines.append("    depends_on_keys:")
            for d in deps:
                lines.append(f"      - {yaml_scalar(d)}")
        else:
            lines.append("    depends_on_keys: []")
        lines.append(f"    severity: {yaml_scalar(c.get('severity'))}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# README + SKILL emit
# ---------------------------------------------------------------------------
def emit_readme(meta, purpose, filer_role, open_questions, ambiguities):
    lines = [
        f"# {meta['form_id']} — {meta['title']}",
        "",
        f"**Entity type:** {meta['entity_type']}  ",
        f"**Statute:** {meta['statute']}  ",
        f"**Source:** {meta['source']}  ",
        f"**Pages:** {meta['num_pages']}  ",
        f"**Fields:** {meta['num_fields']}  ",
        f"**Mapped fields:** {meta['mapped_fields']}  ",
        f"**Filer role:** {filer_role or 'n/a'}",
        "",
        "## Purpose",
        "",
        purpose or "Maine Secretary of State entity filing form.",
        "",
        "## Field mapping",
        "",
        "This directory contains a machine-readable mapping between canonical "
        "data keys and the PDF's AcroForm widget names.",
        "",
        "| File | Purpose |",
        "|------|---------|",
        "| `form.yaml` | Form metadata |",
        "| `mapping.json` | canonical_key to widget mapping |",
        "| `schema.json` | JSON Schema for fill data |",
        "| `fields.csv` | Flat field inventory |",
        "| `rubric.yaml` | Validation checks |",
        "| `README.md` | This file |",
        "| `SKILL.md` | Agent fill guidance |",
        "",
        "## Known ambiguities",
        "",
    ]
    notes = list(ambiguities) + [f"Open question: {q}" for q in (open_questions or [])]
    if notes:
        for n in notes:
            lines.append(f"- {n}")
    else:
        lines.append("- None recorded.")
    lines.append("")
    return "\n".join(lines)


def emit_skill(meta, purpose, mapping, rubric_checks):
    fields = mapping["fields"]
    # key field table (cap at 12 for readability, prioritise high confidence)
    rows = sorted(
        fields.items(),
        key=lambda kv: (-CONF_RANK.get(kv[1].get("confidence", "low"), 1), kv[0]),
    )[:12]

    lines = [
        f"# SKILL: Filling {meta['form_id']}",
        "",
        f"**Form:** {meta['title']}  ",
        f"**Entity type:** {meta['entity_type']}  ",
        f"**When to use:** {purpose or 'Maine SoS entity filing.'}",
        "",
        "## Canonical fields",
        "",
        "| Key | Type | Confidence | Notes |",
        "|-----|------|-----------|-------|",
    ]
    for key, spec in rows:
        note = spec.get("label", "")
        if isinstance(spec.get("widget_id"), list):
            note = (note + " (fills multiple widgets)").strip()
        lines.append(
            f"| `{key}` | {spec.get('field_type', 'text')} | "
            f"{spec.get('confidence', 'low')} | {note} |"
        )

    lines += ["", "## Conditional logic", ""]
    cond = [c for c in rubric_checks if c.get("severity") in ("error", "required")]
    if cond:
        for c in cond:
            deps = ", ".join(f"`{d}`" for d in (c.get("depends_on_keys") or []))
            lines.append(f"- {c.get('description')} (depends on {deps})")
    else:
        lines.append("- No conditional rules recorded; fill the mapped fields directly.")

    # example case data: pick a few representative keys
    example = build_example(fields)
    lines += [
        "",
        "## Example case data",
        "",
        "```json",
        json.dumps(example, indent=2, ensure_ascii=False),
        "```",
        "",
    ]
    return "\n".join(lines)


def build_example(fields):
    """Synthetic minimal example dict from a form's mapped keys."""
    example = {}
    sample_count = 0
    for key, spec in fields.items():
        if sample_count >= 8:
            break
        ft = spec.get("field_type", "text")
        val = sample_value(key, ft)
        assign_nested(example, key, val)
        sample_count += 1
    return example


def sample_value(key, field_type):
    last = key.split(".")[-1]
    if field_type == "checkbox":
        return True
    if "name" in last:
        return "Wabanaki Widgets, Inc." if key.startswith("entity") else "Sample Value"
    if "date" in last:
        return "2026-01-15"
    if "number" in last or "cra" in last:
        return "P99999"
    if "count" in last or "shares" in last:
        return 100
    return "Sample Value"


def assign_nested(root, dotted_key, value):
    parts = [p for p in dotted_key.replace("[]", "").split(".") if p]
    cur = root
    for i, p in enumerate(parts):
        if i == len(parts) - 1:
            cur[p] = value
        else:
            cur = cur.setdefault(p, {})


# ---------------------------------------------------------------------------
# fields.csv
# ---------------------------------------------------------------------------
def write_fields_csv(path, field_mappings):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["widget_id", "page", "field_type", "label_verbatim",
                    "canonical_key", "confidence", "rationale"])
        for m in field_mappings:
            key = m.get("proposed_canonical_key") or ""
            wid = m.get("field_id") or ""
            ft = infer_field_type(key, wid, m.get("nearby_label_text", ""))
            w.writerow([
                wid,
                m.get("page", ""),
                ft,
                m.get("nearby_label_text", ""),
                key,
                m.get("confidence", ""),
                m.get("rationale", ""),
            ])


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------
def build(pdf_dir, pass1_dir, repo_root, overwrite_hand_maintained=False):
    pdf_dir = Path(pdf_dir)
    pass1_dir = Path(pass1_dir)
    repo_root = Path(repo_root)
    forms_root = repo_root / "forms"
    catalog_root = repo_root / "catalog"
    docs_root = repo_root / "docs"
    forms_root.mkdir(parents=True, exist_ok=True)
    catalog_root.mkdir(parents=True, exist_ok=True)
    docs_root.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(p for p in pdf_dir.glob("*.pdf"))
    hand_maintained = load_hand_maintained()
    forms_index = []
    pdf_manifest = {}
    by_entity = defaultdict(list)
    status_rows = []
    mismatch_report = []
    conf_totals = {"high": 0, "medium": 0, "low": 0}
    total_mapped = 0

    for pdf_path in pdfs:
        form_id = pdf_path.stem
        if form_id in hand_maintained and not overwrite_hand_maintained:
            print(f"skipping hand-maintained {form_id}")
            continue
        pass1_path = pass1_dir / f"{form_id}.json"
        if not pass1_path.exists():
            mismatch_report.append((form_id, "MISSING pass1 JSON"))
            continue
        pass1 = json.loads(pass1_path.read_text(encoding="utf-8"))
        parsed = pass1.get("parsed", {})
        field_mappings = parsed.get("field_mappings", [])
        schema_gaps = parsed.get("schema_gaps", [])
        rubric_checks = parsed.get("draft_rubric_checks", [])
        open_questions = parsed.get("open_questions", [])
        purpose = parsed.get("form_purpose", "")
        filer_role = parsed.get("filer_role", "")

        entity_label, statute = entity_meta(form_id)
        num_pages, pdf_fields, has_acro = pdf_info(pdf_path)

        form_dir = forms_root / form_id
        form_dir.mkdir(parents=True, exist_ok=True)

        # copy pdf
        shutil.copyfile(pdf_path, form_dir / f"{form_id}.pdf")

        # mapping
        mapping = build_mapping(form_id, field_mappings)
        mapped_count = len(mapping["fields"])
        total_mapped += mapped_count

        # confidence tally
        for spec in mapping["fields"].values():
            c = spec.get("confidence", "low")
            if c in conf_totals:
                conf_totals[c] += 1

        # widget cross-check
        mapped_widgets = set()
        for spec in mapping["fields"].values():
            w = spec["widget_id"]
            if isinstance(w, list):
                mapped_widgets.update(w)
            else:
                mapped_widgets.add(w)
        missing_in_pdf = sorted(w for w in mapped_widgets if w not in pdf_fields)
        unmapped_in_pdf = sorted(pdf_fields - mapped_widgets)
        if missing_in_pdf:
            mismatch_report.append(
                (form_id, "mapping references widgets not in PDF: "
                 + ", ".join(missing_in_pdf[:10])
                 + (" ..." if len(missing_in_pdf) > 10 else ""))
            )

        meta = {
            "form_id": form_id,
            "code": bare_code(form_id),
            "title": pass1.get("form_name", form_id),
            "entity_type": entity_label,
            "statute": statute,
            "num_pages": num_pages,
            "num_fields": len(pdf_fields),
            "mapped_fields": mapped_count,
            "source": "Maine Secretary of State",
            "revision": None,
            "jurisdiction": "Maine",
            "language": "en",
        }

        # write artifacts
        (form_dir / "form.yaml").write_text(emit_form_yaml(meta), encoding="utf-8")
        # mapping.json ships in the canonical (field-id-keyed) direction
        # shared with the sibling repos; the generator's internal shape is
        # converted losslessly at the boundary (engine/mapping.py).
        (form_dir / "mapping.json").write_text(
            json.dumps(mapping_mod.invert(mapping), indent=2,
                       ensure_ascii=False) + "\n", encoding="utf-8")
        schema = build_schema(form_id, schema_gaps,
                              list(mapping["fields"].keys()), rubric_checks)
        (form_dir / "schema.json").write_text(
            json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        write_fields_csv(form_dir / "fields.csv", field_mappings)
        (form_dir / "rubric.yaml").write_text(emit_rubric_yaml(rubric_checks), encoding="utf-8")

        ambiguities = []
        for key, spec in mapping["fields"].items():
            if isinstance(spec["widget_id"], list):
                ambiguities.append(
                    f"`{key}` maps to {len(spec['widget_id'])} widgets; all receive the same value.")
        low_conf = [k for k, s in mapping["fields"].items() if s.get("confidence") == "low"]
        if low_conf:
            ambiguities.append(
                f"{len(low_conf)} low-confidence mapping(s) need human review: "
                + ", ".join(f"`{k}`" for k in low_conf[:6])
                + (" ..." if len(low_conf) > 6 else ""))
        (form_dir / "README.md").write_text(
            emit_readme(meta, purpose, filer_role, open_questions, ambiguities), encoding="utf-8")
        (form_dir / "SKILL.md").write_text(
            emit_skill(meta, purpose, mapping, rubric_checks), encoding="utf-8")

        # catalog entries
        forms_index.append({
            "form_id": form_id,
            "code": meta["code"],
            "title": meta["title"],
            "entity_type": entity_label,
            "statute": statute,
            "num_pages": num_pages,
            "num_fields": len(pdf_fields),
            "mapped_fields": mapped_count,
            "path": f"forms/{form_id}",
        })
        pdf_manifest[form_id] = {
            "filename": f"{form_id}.pdf",
            "sha256": sha256_of(form_dir / f"{form_id}.pdf"),
            "bytes": (form_dir / f"{form_id}.pdf").stat().st_size,
            "num_pages": num_pages,
            "has_acroform": bool(has_acro),
        }
        by_entity[entity_label].append(form_id)
        status_rows.append({
            "form_id": form_id,
            "pages": num_pages,
            "widgets": len(pdf_fields),
            "mapped": mapped_count,
            "missing_in_pdf": len(missing_in_pdf),
            "unmapped_in_pdf": len(unmapped_in_pdf),
        })

    # ---- catalog files ----
    forms_index.sort(key=lambda e: e["form_id"])
    (catalog_root / "forms_index.json").write_text(
        json.dumps({"forms": forms_index}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Shared {"forms": {...}} manifest dialect (maine_forms_engine.specs
    # schema). The source URL + fetch flag are not derivable from the PDFs
    # themselves, so a regeneration carries them over from the existing
    # manifest instead of clobbering them.
    manifest_path = catalog_root / "pdf_manifest.json"
    prior = {}
    if manifest_path.exists():
        prior = json.loads(manifest_path.read_text(encoding="utf-8")).get("forms", {})
    for fid, entry in pdf_manifest.items():
        for carry in ("url", "fetch"):
            if carry in prior.get(fid, {}):
                entry[carry] = prior[fid][carry]
    manifest_path.write_text(
        json.dumps({"count": len(pdf_manifest),
                    "forms": {k: pdf_manifest[k] for k in sorted(pdf_manifest)}},
                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    by_entity_out = {
        "by_entity_type": {
            et: {"count": len(ids), "form_ids": sorted(ids)}
            for et, ids in sorted(by_entity.items())
        }
    }
    (catalog_root / "by_entity.json").write_text(
        json.dumps(by_entity_out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- STATUS.md ----
    write_status(docs_root / "STATUS.md", status_rows, mismatch_report,
                 conf_totals, total_mapped)

    # ---- summary to stdout ----
    summary = {
        "forms": len(forms_index),
        "total_mapped_fields": total_mapped,
        "avg_fields_per_form": round(total_mapped / len(forms_index), 1) if forms_index else 0,
        "confidence": conf_totals,
        "forms_with_widget_mismatches": sum(1 for f, _ in mismatch_report if True),
        "by_entity": {et: len(ids) for et, ids in by_entity.items()},
    }
    return summary, mismatch_report


def write_status(path, rows, mismatch_report, conf_totals, total_mapped):
    rows.sort(key=lambda r: r["form_id"])
    total_widgets = sum(r["widgets"] for r in rows)
    forms_with_mismatch = len([1 for _, msg in mismatch_report if "widgets not in PDF" in msg])
    lines = [
        "# STATUS",
        "",
        "Coverage and validation report. Generated by `tools/build_from_pass1.py`.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Forms | {len(rows)} |",
        f"| Total AcroForm widgets | {total_widgets} |",
        f"| Total mapped keys | {total_mapped} |",
        f"| High-confidence mappings | {conf_totals['high']} |",
        f"| Medium-confidence mappings | {conf_totals['medium']} |",
        f"| Low-confidence mappings | {conf_totals['low']} |",
        f"| Forms with widget mismatches | {forms_with_mismatch} |",
        "",
        "## Per-form coverage",
        "",
        "| Form | Pages | Widgets | Mapped | Widgets missing from PDF | PDF widgets unmapped |",
        "|------|-------|---------|--------|--------------------------|----------------------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['form_id']} | {r['pages']} | {r['widgets']} | {r['mapped']} "
            f"| {r['missing_in_pdf']} | {r['unmapped_in_pdf']} |")
    lines += ["", "## Mismatches", ""]
    real = [(f, m) for f, m in mismatch_report]
    if real:
        for f, m in real:
            lines.append(f"- **{f}**: {m}")
    else:
        lines.append("(none)")
    lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf-dir", default=os.environ.get("SOS_PDF_DIR"),
                    help="directory of blank SoS AcroForm PDFs")
    ap.add_argument("--pass1-dir", default=os.environ.get("SOS_PASS1_DIR"),
                    help="directory of pass-1 mapping JSON files")
    ap.add_argument("--repo-root", default=str(Path(__file__).resolve().parent.parent),
                    help="repository root to write artifacts into")
    ap.add_argument("--force", "--overwrite-hand-maintained", dest="force",
                    action="store_true",
                    help="also regenerate hand-maintained forms "
                         "(see tools/HAND_MAINTAINED.txt; clobbers reconciled artifacts)")
    args = ap.parse_args(argv)
    if not args.pdf_dir or not args.pass1_dir:
        ap.error("--pdf-dir and --pass1-dir are required (or set SOS_PDF_DIR / SOS_PASS1_DIR)")

    summary, mismatches = build(args.pdf_dir, args.pass1_dir, args.repo_root,
                                overwrite_hand_maintained=args.force)
    print(json.dumps(summary, indent=2))
    print(f"\nMismatch entries: {len(mismatches)}")
    for f, m in mismatches[:15]:
        print(f"  {f}: {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
