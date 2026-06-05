"""Deterministic PDF accessibility remediation for the SoS forms.

See ``remediate_form.py``. Honest scope: form-field tooltips (``/TU``) from the
schema labels, document title, language, and DisplayDocTitle. A full PDF/UA tag
tree (StructTreeRoot) needs an authoring tool and is intentionally NOT faked.
"""
from .remediate_form import remediate, remediate_to_path  # noqa: F401

__all__ = ["remediate", "remediate_to_path"]
