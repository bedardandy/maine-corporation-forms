"""Canonical-direction ``mapping.json`` dialect: load, invert, round-trip.

The sibling forms repos key their ``mapping.json`` by the **PDF AcroForm
field** (``map: {field_id: canonical_key}``); this repo historically keyed by
the **canonical case key** (``fields: {canonical_key: {widget_id, ...}}``).
Same data, inverted direction. This module converges the repo on the shared,
PDF-anchored direction while keeping every per-binding fact this repo records
(field types, option bindings, ``when`` gates, confidence, labels):

    {
      "form_id": "LLC_MLLC-6",
      "map": {
        "<field_id>": {
          "key": "<canonical case key>",
          ... the rest of the binding spec, verbatim ...
        },
        ...
      }
    }

``<field_id>`` is the AcroForm field the binding anchors on:

- a text / checkbox widget name, or a radio *group* name (``options`` then
  maps each enum value to an on-state, not a widget);
- for a multi-widget fan-out (one value replicated into several widgets) the
  first widget, with the full ordered list kept under ``"widgets"``;
- for ``enum_select`` / ``enum_text_select`` (choose-one groups with no group
  field) the first option widget; ``options`` (enum value -> widget) carries
  the real per-widget binding.

The inversion is **lossless and idempotent**: :func:`revert` reconstructs the
legacy ``fields`` dict exactly (dict equality), :func:`invert` of a
canonical-direction mapping is a no-op copy, and
``invert(revert(m)) == m``. ``tools/convert_mapping_direction.py`` is the CLI;
``tests/test_mapping_direction.py`` pins the invariants for every form.

Consumers iterate bindings through :func:`entries`, which presents the
familiar ``{canonical_key: spec}`` view (``spec`` carries ``widget_id`` /
``options`` exactly as before), so resolution semantics are unchanged.
"""
import copy
import json
from pathlib import Path

#: choose-one groups bound through ``options`` (enum value -> widget); they
#: carry no ``widget_id`` of their own.
ENUM_GROUP_TYPES = ("enum_select", "enum_text_select")


def is_canonical(mapping):
    """True when ``mapping`` is in the shared field-id-keyed direction."""
    return "map" in mapping and "fields" not in mapping


def _anchor_field_id(key, spec):
    """The AcroForm field a legacy entry anchors on (see module docstring)."""
    wid = spec.get("widget_id")
    if isinstance(wid, list):
        if not wid:
            raise ValueError(f"entry {key!r}: empty widget_id list")
        if spec.get("field_type") in ENUM_GROUP_TYPES:
            raise ValueError(
                f"entry {key!r}: {spec.get('field_type')} with a widget_id "
                "list is not representable; bind through options only")
        return wid[0]
    if wid:
        if spec.get("field_type") in ENUM_GROUP_TYPES:
            raise ValueError(
                f"entry {key!r}: {spec.get('field_type')} with a widget_id "
                "is not representable; bind through options only")
        return wid
    if spec.get("field_type") in ENUM_GROUP_TYPES:
        options = spec.get("options") or {}
        for widget in options.values():
            return widget
        raise ValueError(f"entry {key!r}: enum group with empty options")
    raise ValueError(f"entry {key!r}: no widget_id or options binding")


def invert(mapping):
    """Legacy ``fields``-keyed mapping -> canonical ``map``-keyed mapping.

    A mapping already in the canonical direction is returned as a deep copy
    (idempotent). Raises ``ValueError`` on an anchor collision (two entries
    anchoring on one field id) — none exist in this repo; a new one would
    need a dialect extension, not a silent merge.
    """
    if is_canonical(mapping):
        return copy.deepcopy(mapping)
    out = {}
    for top_key, top_val in mapping.items():
        if top_key != "fields":
            out[top_key] = copy.deepcopy(top_val)
            continue
        m = {}
        for key, spec in (top_val or {}).items():
            fid = _anchor_field_id(key, spec)
            if fid in m:
                raise ValueError(
                    f"field id {fid!r} anchors both {m[fid]['key']!r} and "
                    f"{key!r}; cannot invert losslessly")
            binding = {"key": key}
            wid = spec.get("widget_id")
            if isinstance(wid, list):
                binding["widgets"] = copy.deepcopy(wid)
            for sk, sv in spec.items():
                if sk == "widget_id":
                    continue
                if sk in ("key", "widgets"):
                    raise ValueError(
                        f"entry {key!r}: spec key {sk!r} collides with the "
                        "canonical-direction dialect")
                binding[sk] = copy.deepcopy(sv)
            m[fid] = binding
        out["map"] = m
    return out


def revert(mapping):
    """Canonical ``map``-keyed mapping -> legacy ``fields``-keyed mapping.

    The exact inverse of :func:`invert` (used by the round-trip tests and by
    :func:`entries`). A legacy mapping is returned as a deep copy.
    """
    if not is_canonical(mapping):
        return copy.deepcopy(mapping)
    out = {}
    for top_key, top_val in mapping.items():
        if top_key != "map":
            out[top_key] = copy.deepcopy(top_val)
            continue
        out["fields"] = _entries_of_map(top_val)
    return out


def _entries_of_map(m):
    fields = {}
    for fid, binding in (m or {}).items():
        if "key" not in binding:
            raise ValueError(f"binding for field {fid!r} has no 'key'")
        key = binding["key"]
        if key in fields:
            raise ValueError(f"duplicate canonical entry {key!r}")
        rest = {k: copy.deepcopy(v) for k, v in binding.items()
                if k not in ("key", "widgets")}
        spec = {}
        if "canonical_key" in rest:
            spec["canonical_key"] = rest.pop("canonical_key")
        if "widgets" in binding:
            spec["widget_id"] = copy.deepcopy(binding["widgets"])
        elif rest.get("field_type") not in ENUM_GROUP_TYPES:
            spec["widget_id"] = fid
        spec.update(rest)
        fields[key] = spec
    return fields


def entries(mapping):
    """``{canonical_key: spec}`` view of a canonical-direction mapping.

    ``spec`` is the familiar legacy shape (``widget_id`` scalar or list,
    ``options``, ``when``, ``field_type``, ...), so every consumer resolves
    bindings exactly as before the direction flip. Raises on a legacy
    ``fields``-keyed mapping — the repo must never be mixed-direction.
    """
    if not isinstance(mapping, dict):
        raise ValueError(f"mapping must be a dict (got {type(mapping).__name__})")
    if "fields" in mapping:
        raise ValueError(
            "legacy canonical-key-keyed mapping.json (top-level 'fields'); "
            "convert it with tools/convert_mapping_direction.py")
    return _entries_of_map(mapping.get("map"))


def load_mapping(form_id, forms_root="forms"):
    """Load ``forms/<FORM_ID>/mapping.json`` (canonical direction enforced)."""
    path = Path(forms_root) / form_id / "mapping.json"
    mapping = json.loads(path.read_text(encoding="utf-8"))
    if "fields" in mapping:
        raise ValueError(
            f"{path}: legacy canonical-key-keyed mapping.json; "
            "convert it with tools/convert_mapping_direction.py")
    return mapping
