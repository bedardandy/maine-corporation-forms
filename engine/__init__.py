"""maine-corporation-forms fill engine."""
from . import canonical, fill, plan, route, schema, verify  # noqa: F401

__all__ = ["canonical", "fill", "plan", "route", "schema", "verify"]

# Optional: print-ready copies (bake appearances, spill overflow to schedules,
# flatten). Depends on PyMuPDF; keep optional so the core engine imports without
# it.
try:  # pragma: no cover - optional dependency
    from . import printcopy  # noqa: F401

    __all__.append("printcopy")
except ImportError:
    printcopy = None
