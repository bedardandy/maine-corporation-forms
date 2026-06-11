"""Vendor-neutral fill model derived from a Maine SoS form's mapping + schema.

This is the single normalization layer the exporters build on. It turns a form's
``mapping.json`` (the authoritative canonical-key -> AcroForm-widget list) and
``schema.json`` (types + enums) into a flat list of ``ExportField`` records with
a small, stable vocabulary that maps cleanly onto third-party templating systems
(DocuSign, PandaDoc, HotDocs, Clio Draft, Gavel, XFDF, ...).

Unlike the probate sibling, these forms are **AcroForm-native**: each canonical
key already binds to one or more real PDF field names (``widget_id``). The model
exposes both — ``field_id`` (the canonical input key, the data contract) and
``acroform_names`` (the real PDF field names, the import handle). The runtime
field-split (see ``engine.fill.split_shared_fields``) renames a shared widget to
``<T>__p<page>`` at fill time only; the official PDF keeps the base name, so the
de-promoted base name is what an XFDF/e-sign template must reference. ``_acroform_name``
strips the ``__p<page>`` suffix for that reason.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

try:
    import yaml
except ImportError:  # pragma: no cover - PyYAML is a declared dependency
    yaml = None


# Canonical data-binding buckets. These SoS forms are deterministic AcroForm
# fills: there are no LLM-composed or formula fields, so every field is either a
# real data input or a checkbox/enum selection. The full vocabulary is kept so
# the exporters match the probate sibling and tolerate future bindings.
BIND_DATA = "data"            # a real input value (text / number / date)
BIND_ENUM = "enum"            # a radio group or enum-constrained selection
BIND_BOOLEAN = "boolean"      # a checkbox
BIND_SIGNATURE = "signature"  # a wet-ink signature line
BIND_COMPUTED = "computed"    # derived/formula (none today; reserved)


_PROMOTED = re.compile(r"__p\d+(?:_\d+)?$")


def _acroform_name(widget_id: str) -> str:
    """Return the real PDF field name for a (possibly promoted) widget id.

    The fill engine promotes a shared ``/Btn`` kid to ``<T>__p<page>`` in memory
    only; the official PDF keeps ``<T>``. Templates that import into the official
    PDF must use the base name.
    """
    return _PROMOTED.sub("", str(widget_id))


@dataclass
class ExportField:
    field_id: str                 # canonical dotted key (the data contract)
    acroform_names: list          # real PDF field name(s) (the import handle)
    label: str
    data_type: str                # string | integer | number | boolean | date | enum
    binding: str                  # one of the BIND_* buckets
    required: bool = False
    when: str | None = None       # conditional gate (raw expression from mapping)
    enum: list | None = None
    page: int | None = None
    confidence: str | None = None


@dataclass
class FormModel:
    form_id: str
    title: str
    fields: list
    source_url: str | None = None
    signature_mode: str = "wet_ink"

    def by_binding(self, binding: str) -> list:
        return [f for f in self.fields if f.binding == binding]


def _norm_type(raw):
    t = (raw or "string").lower()
    if t in ("str", "text", "string"):
        return "string"
    if t in ("int", "integer"):
        return "integer"
    if t in ("float", "number", "decimal"):
        return "number"
    if t in ("bool", "boolean", "checkbox"):
        return "boolean"
    if t in ("date", "datetime"):
        return "date"
    if t in ("enum", "select", "select_one", "radio", "choice"):
        return "enum"
    return "string"


def _schema_leaf(schema, dotted):
    """Resolve a dotted canonical key to its schema leaf node, or None.

    Indices (``entities[0]`` / ``parties[*]``) are stripped before walking.
    """
    cur = schema.get("properties", {})
    node = None
    for part in re.sub(r"\[[^\]]*\]", "", dotted).split("."):
        if part not in cur:
            return None
        node = cur[part]
        cur = node.get("properties", {}) if node.get("type") == "object" else {}
    return node


_DATE_HINT = re.compile(r"(?:^|[._])date(?:[._]|$)|date_signed|_date$", re.I)


def _data_type(spec, leaf, field_id):
    """Pick the neutral data type from the mapping spec + schema leaf."""
    ftype = spec.get("field_type", "text")
    if ftype == "radio":
        return "enum"
    if ftype in ("checkbox", "boolean"):
        return "boolean"
    if leaf is not None:
        if leaf.get("enum"):
            return "enum"
        t = _norm_type(leaf.get("type"))
        if t != "string":
            return t
    # text field: promote obvious dates so e-sign/gavel pick a date control
    if _DATE_HINT.search(field_id):
        return "date"
    return "string"


def _binding(data_type, field_id):
    if data_type == "boolean":
        return BIND_BOOLEAN
    if data_type == "enum":
        return BIND_ENUM
    if field_id.endswith(".signature") or field_id.endswith("_signature"):
        return BIND_SIGNATURE
    return BIND_DATA


def _required_keys(form_dir):
    """Canonical keys named by a ``severity: required`` rubric check."""
    path = form_dir / "rubric.yaml"
    if not path.exists() or yaml is None:
        return set()
    rubric = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    keys = set()
    for check in rubric.get("checks") or []:
        if check.get("severity") == "required":
            keys.update(check.get("depends_on_keys") or [])
    return keys


def _acroform_names(widget_id):
    ids = widget_id if isinstance(widget_id, list) else [widget_id]
    seen, out = set(), []
    for w in ids:
        name = _acroform_name(w)
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


def build_model(form_id, repo_root):
    """Build a :class:`FormModel` for ``form_id`` from its mapping + schema."""
    import pathlib
    import sys
    repo_root = pathlib.Path(repo_root)
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))  # for engine.mapping
    from engine.mapping import entries as mapping_entries
    form_dir = repo_root / "forms" / form_id
    mapping = json.loads((form_dir / "mapping.json").read_text(encoding="utf-8"))
    schema = {}
    schema_path = form_dir / "schema.json"
    if schema_path.exists():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    meta = {}
    meta_path = form_dir / "form.yaml"
    if meta_path.exists() and yaml is not None:
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    required = _required_keys(form_dir)

    fields = []
    for key, spec in mapping_entries(mapping).items():
        leaf = _schema_leaf(schema, key) if schema else None
        dt = _data_type(spec, leaf, key)
        enum = (leaf or {}).get("enum")
        if enum is None and spec.get("field_type") == "radio":
            enum = sorted((spec.get("options") or {}).keys()) or None
        fields.append(ExportField(
            field_id=key,
            acroform_names=_acroform_names(spec.get("widget_id")),
            label=spec.get("label", key),
            data_type=dt,
            binding=_binding(dt, key),
            required=key in required,
            when=spec.get("when"),
            enum=enum,
            page=spec.get("page"),
            confidence=spec.get("confidence"),
        ))

    title = meta.get("title") or schema.get("title") or form_id
    signature_mode = "wet_ink"
    try:
        from tools import signer_rules

        signature_mode = signer_rules.rules_for(form_id).get(
            "signature_mode", "wet_ink"
        )
    except Exception:
        pass
    return FormModel(
        form_id=form_id,
        title=title,
        source_url=(meta.get("source_url") or mapping.get("source_url")
                    or schema.get("source_url")),
        fields=fields,
        signature_mode=signature_mode,
    )
