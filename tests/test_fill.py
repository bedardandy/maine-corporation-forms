"""Fill-engine behavior against a synthetic blank, so no official PDF is needed.

Builds a tiny AcroForm PDF with plain text widgets in ``tmp_path``, fills it
through the real ``engine.fill`` pipeline (``verify_blank="off"`` since the
synthetic form is not in the manifest), and reads the values back with pypdf.
"""
import io
import json
import sys
from pathlib import Path

import pypdf
from pypdf.generic import (
    ArrayObject,
    DictionaryObject,
    NameObject,
    RectangleObject,
    TextStringObject,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import fill  # noqa: E402

FORM_ID = "TEST_WHEN"


def _make_blank(path, field_names):
    """Write a one-page PDF with one text widget per name in ``field_names``."""
    writer = pypdf.PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    fields = ArrayObject()
    annots = ArrayObject()
    for i, name in enumerate(field_names):
        widget = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Tx"),
            NameObject("/T"): TextStringObject(name),
            NameObject("/Rect"): RectangleObject(
                [50, 700 - 30 * i, 250, 720 - 30 * i]),
            NameObject("/P"): page.indirect_reference,
        })
        ref = writer._add_object(widget)
        fields.append(ref)
        annots.append(ref)
    page[NameObject("/Annots")] = annots
    acroform = DictionaryObject({NameObject("/Fields"): fields})
    writer._root_object[NameObject("/AcroForm")] = writer._add_object(acroform)
    with open(path, "wb") as fh:
        writer.write(fh)


def _form_root(tmp_path):
    """A forms_root containing one synthetic form with two when-gated fields."""
    d = tmp_path / FORM_ID
    d.mkdir()
    _make_blank(d / f"{FORM_ID}.pdf", ["TextA", "TextCom", "TextNoncom"])
    mapping = {
        "form_id": FORM_ID,
        "fields": {
            "entity.name": {"widget_id": "TextA", "field_type": "text"},
            "registered_agent.commercial_name": {
                "widget_id": "TextCom", "field_type": "text",
                "when": "registered_agent.type == 'commercial'",
            },
            "registered_agent.noncommercial_name": {
                "widget_id": "TextNoncom", "field_type": "text",
                "when": "registered_agent.type == 'noncommercial'",
            },
        },
    }
    (d / "mapping.json").write_text(json.dumps(mapping))
    return str(tmp_path)


def _filled_values(forms_root, case):
    buf = io.BytesIO()
    fill.fill_to_stream(FORM_ID, case, buf, forms_root, verify_blank="off")
    buf.seek(0)
    return pypdf.PdfReader(buf).get_form_text_fields()


def test_fill_skips_when_gated_off(tmp_path):
    forms_root = _form_root(tmp_path)
    case = {
        "entity": {"name": "Acme, LLC"},
        "registered_agent": {
            "type": "noncommercial",
            "commercial_name": "MUST NOT APPEAR",
            "noncommercial_name": "Jane Agent",
        },
    }
    values = _filled_values(forms_root, case)
    assert values.get("TextA") == "Acme, LLC"
    assert not values.get("TextCom"), \
        "field gated off by `when` was written anyway"
    assert values.get("TextNoncom") == "Jane Agent"


def test_fill_writes_when_gate_true(tmp_path):
    forms_root = _form_root(tmp_path)
    case = {
        "entity": {"name": "Acme, LLC"},
        "registered_agent": {"type": "commercial",
                             "commercial_name": "CSC of Maine"},
    }
    values = _filled_values(forms_root, case)
    assert values.get("TextCom") == "CSC of Maine"
    assert not values.get("TextNoncom")


def test_fill_keeps_field_when_controller_unknown(tmp_path):
    # Conservative gating, same as engine.plan: when the controller is absent
    # the condition is unknown (None, not False) and the field still fills.
    forms_root = _form_root(tmp_path)
    case = {"registered_agent": {"commercial_name": "Maybe Commercial"}}
    values = _filled_values(forms_root, case)
    assert values.get("TextCom") == "Maybe Commercial"
