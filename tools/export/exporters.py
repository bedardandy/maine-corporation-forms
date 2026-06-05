"""Vendor-specific exporters over the neutral :class:`FormModel`.

Each exporter takes a ``FormModel`` and returns ``{filename: serialized_content}``.
The CLI (``export_form.py``) writes them to disk. Per-vendor specifics are kept to
TYPE TABLES and small shaping helpers, not control flow, so a new target is a
table plus a function.

Because these forms are AcroForm-native, the **import handles** differ by target:

- XFDF and DocuSign/PandaDoc anchor on the real **AcroForm field name**
  (``acroform_names``) so the artifact imports into the official PDF.
- The data dictionary, case schema, doc-assembly merge tokens, and Gavel
  variables key on the **canonical ``field_id``** — the stable data contract an
  integrator binds their matter data to.

Targets:
  - interchange : template.xfdf + data_dictionary.csv + case_schema.json
  - esign       : docusign_template.json + pandadoc_fields.json
  - docassembly : variables.json + merge_tokens.csv + logic.md
  - gavel       : gavel_variables.json
"""
from __future__ import annotations

import csv
import io
import json

from .model import (
    BIND_BOOLEAN, BIND_DATA, BIND_ENUM, BIND_SIGNATURE, FormModel,
)


# ---- shared helpers -------------------------------------------------------

def _xml_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def _esign_kind(f):
    """DocuSign/PandaDoc control kind for a field."""
    if f.binding == BIND_SIGNATURE:
        return "signHere"
    if f.data_type == "boolean":
        return "checkbox"
    return "text"


# ---- interchange (XFDF + data dictionary + JSON schema) --------------------

def export_interchange(model: FormModel) -> dict:
    # XFDF keys on the real AcroForm field name so it imports into the official
    # PDF. One <field> per distinct AcroForm name across fillable fields.
    seen = set()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve">',
             "  <fields>"]
    for f in model.fields:
        for name in f.acroform_names:
            if name in seen:
                continue
            seen.add(name)
            lines.append(f'    <field name="{_xml_escape(name)}">')
            lines.append("      <value></value>")
            lines.append("    </field>")
    lines.append("  </fields>")
    lines.append("</xfdf>")
    xfdf = "\n".join(lines)

    # data dictionary CSV — canonical key + the AcroForm name(s) it drives.
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["field_id", "acroform_field", "type", "binding", "required",
                "enum", "when", "page", "confidence"])
    for f in model.fields:
        w.writerow([f.field_id, "|".join(f.acroform_names), f.data_type,
                    f.binding, f.required, "|".join(f.enum) if f.enum else "",
                    f.when or "", "" if f.page is None else f.page,
                    f.confidence or ""])
    data_dict = buf.getvalue()

    # case JSON schema keyed by canonical field_id (the input contract).
    props, required = {}, []
    for f in model.fields:
        p = {"type": "string" if f.data_type in ("date", "enum")
             else f.data_type}
        if f.enum:
            p["enum"] = f.enum
        if f.label:
            p["description"] = f.label
        props[f.field_id] = p
        if f.required and not f.when:
            required.append(f.field_id)
    case_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{model.form_id} case data",
        "type": "object",
        "properties": props,
        "required": required,
    }
    return {
        "template.xfdf": xfdf,
        "data_dictionary.csv": data_dict,
        "case_schema.json": json.dumps(case_schema, indent=2),
    }


# ---- esign (DocuSign + PandaDoc) ------------------------------------------

def export_esign(model: FormModel) -> dict:
    # Maine SoS filings are wet-ink by default. When the form's signature_mode is
    # wet_ink we do NOT emit a real signHere tab -- that would imply an
    # electronic signature is acceptable for filing. The signature is routed to a
    # text tab carrying a wet-ink note, and a wet_ink_warning is added, so the
    # map stays usable for internal routing/approval.
    wet_ink = getattr(model, "signature_mode", "wet_ink") == "wet_ink"
    wet_note = "WET INK REQUIRED - sign the printed form by hand"
    ds_tabs = {"textTabs": [], "checkboxTabs": [], "signHereTabs": []}
    pd_fields = []
    for f in model.fields:
        kind = _esign_kind(f)
        sign_blocked = kind == "signHere" and wet_ink
        # Anchor on the real AcroForm field name; one tab per name.
        for name in f.acroform_names:
            tab = {"tabLabel": name, "anchorString": name,
                   "conditionalParentField": None}
            if f.when:
                tab["conditionalParentField"] = f.when
            if kind == "signHere" and not wet_ink:
                ds_tabs["signHereTabs"].append(tab)
            elif kind == "checkbox":
                ds_tabs["checkboxTabs"].append(tab)
            else:
                if sign_blocked:
                    tab["note"] = wet_note
                ds_tabs["textTabs"].append(tab)
        pd_fields.append({
            "name": f.field_id,
            "acroform_field": f.acroform_names[0] if f.acroform_names else None,
            "title": f.label,
            "type": ("signature" if kind == "signHere" and not wet_ink
                     else "checkbox" if kind == "checkbox" else "field"),
            "required": f.required,
            **({"note": wet_note} if sign_blocked else {}),
            **({"merge_field": f.field_id} if kind != "signHere" else {}),
        })
    ds_payload = {"tabs": ds_tabs}
    pd_payload = {"fields": pd_fields}
    if wet_ink:
        warning = ("This Maine SoS filing requires an original wet-ink signature. "
                   "Use this map for routing/approval only; print and hand-sign "
                   "before filing.")
        ds_payload["wet_ink_warning"] = warning
        pd_payload["wet_ink_warning"] = warning
    return {
        "docusign_template.json": json.dumps(ds_payload, indent=2),
        "pandadoc_fields.json": json.dumps(pd_payload, indent=2),
    }


# ---- docassembly (variables + merge tokens + logic) -----------------------

def export_docassembly(model: FormModel) -> dict:
    variables = []
    for f in model.fields:
        v = {"name": f.field_id, "type": f.data_type, "label": f.label}
        if f.enum:
            v["choices"] = f.enum
        if f.when:
            v["show_if"] = f.when
        variables.append(v)
    merge = io.StringIO()
    w = csv.writer(merge)
    w.writerow(["field_id", "clio_token", "mycase_token", "hotdocs_token",
                "gavel_token"])
    for f in model.fields:
        w.writerow([
            f.field_id,
            "{{Matter.Custom." + f.field_id + "}}",
            "[[" + f.field_id + "]]",
            "«" + f.field_id + "»",
            "{{" + f.field_id + "}}",
        ])
    logic = ["# Conditional logic", ""]
    has = False
    for f in model.fields:
        if f.when:
            has = True
            logic.append(f"- **{f.field_id}** is shown when `{f.when}`")
    if not has:
        logic.append("_No conditional fields._")
    return {
        "variables.json": json.dumps({"variables": variables}, indent=2),
        "merge_tokens.csv": merge.getvalue(),
        "logic.md": "\n".join(logic) + "\n",
    }


# ---- gavel ----------------------------------------------------------------

def _gavel_type(f):
    return {"boolean": "checkbox", "date": "date", "integer": "number",
            "number": "number", "enum": "multiple choice"}.get(
                f.data_type, "text")


def export_gavel(model: FormModel) -> dict:
    variables = []
    for f in model.fields:
        gv = {"name": f.field_id, "field_type": _gavel_type(f)}
        if f.enum:
            gv["options"] = [{"label": e, "value": e} for e in f.enum]
        if f.when:
            gv["show_if"] = f.when
        variables.append(gv)
    return {"gavel_variables.json": json.dumps({"variables": variables},
                                               indent=2)}


EXPORTERS = {
    "interchange": export_interchange,
    "esign": export_esign,
    "docassembly": export_docassembly,
    "gavel": export_gavel,
}
