"""Reference exporters: turn a form's mapping + schema into import artifacts for
third-party templating, e-signature, and document-assembly systems.

``model.build_model`` normalizes a form into a vendor-neutral ``FormModel``; the
exporters in ``exporters.py`` consume only that. See ``docs/templating.md``.
"""
from .model import ExportField, FormModel, build_model  # noqa: F401
from .exporters import EXPORTERS  # noqa: F401

__all__ = ["ExportField", "FormModel", "build_model", "EXPORTERS"]
