"""Lightweight JSON-Schema validation for form fill data.

Performs type, required, and enum checks against a form's ``schema.json``.
Intentionally dependency-free (standard library only) and limited to the
subset of JSON Schema this project emits: nested objects, arrays of objects,
and typed leaves with optional ``enum``.
"""
import json
from pathlib import Path

from . import canonical

_JSON_TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
}


def load_schema(form_id, forms_root="forms"):
    path = Path(forms_root) / form_id / "schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate(form_id, case_data, forms_root="forms"):
    """Validate ``case_data`` against a form's schema.

    Returns a list of error strings (empty when valid).
    """
    schema = load_schema(form_id, forms_root)
    return validate_against(schema, case_data)


def validate_against(schema, case_data, path=""):
    errors = []
    if not isinstance(case_data, dict):
        return [f"{path or '<root>'}: expected object"]

    # required (top level of this schema node)
    for req in schema.get("required", []):
        if req not in case_data:
            errors.append(f"{_join(path, req)}: required key missing")

    props = schema.get("properties", {})
    for key, value in case_data.items():
        if key not in props:
            # unknown keys are tolerated (forward-compatible)
            continue
        errors.extend(_validate_value(props[key], value, _join(path, key)))
    return errors


def _validate_value(node, value, path):
    errors = []
    expected = node.get("type")
    if expected and expected in _JSON_TYPE_CHECKS:
        if not _JSON_TYPE_CHECKS[expected](value):
            errors.append(f"{path}: expected {expected}, got {type(value).__name__}")
            return errors
    enum = node.get("enum")
    if enum is not None and value not in enum:
        errors.append(f"{path}: {value!r} not in {enum}")
    if expected == "object":
        errors.extend(validate_against(node, value, path))
    elif expected == "array":
        item_schema = node.get("items", {})
        for i, item in enumerate(value):
            if item_schema.get("type") == "object":
                errors.extend(validate_against(item_schema, item, f"{path}[{i}]"))
            else:
                errors.extend(_validate_value(item_schema, item, f"{path}[{i}]"))
    return errors


def _join(prefix, key):
    return f"{prefix}.{key}" if prefix else key
