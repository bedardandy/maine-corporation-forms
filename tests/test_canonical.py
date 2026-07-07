"""engine.canonical — dotted-path resolver (``get``) and presence (``has``).

Focus: the ``has()`` non-None contract. A key that is present but explicitly
``None`` is *not* a usable value and must return ``False`` (it previously
returned ``True``, contradicting the docstring).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import canonical  # noqa: E402


def test_get_basic_and_missing():
    data = {"a": {"b": {"c": 1}}}
    assert canonical.get(data, "a.b.c") == 1
    assert canonical.get(data, "a.b.x") is None
    assert canonical.get(data, "a.b.x", "dflt") == "dflt"


def test_get_list_index():
    data = {"items": [{"name": "first"}, {"name": "second"}]}
    assert canonical.get(data, "items[0].name") == "first"
    assert canonical.get(data, "items[1].name") == "second"
    assert canonical.get(data, "items[5].name") is None


def test_has_present_nonnull():
    data = {"entity": {"name": "Acme LLC"}}
    assert canonical.has(data, "entity.name") is True


def test_has_missing_key():
    data = {"entity": {"name": "Acme LLC"}}
    assert canonical.has(data, "entity.registered_agent") is False
    assert canonical.has(data, "does.not.exist") is False


def test_has_present_but_none_is_false():
    """Contract regression: present-but-None resolves to a non-usable value,
    so ``has`` must report False (it previously returned True)."""
    data = {"entity": {"name": None, "type": "llc"}}
    assert canonical.has(data, "entity.name") is False
    # a sibling with a real value is still present
    assert canonical.has(data, "entity.type") is True


def test_has_falsy_but_present_values_are_true():
    """Only None is treated as absent — other falsy-but-set values (empty
    string, 0, False, empty list) are still 'present' per the non-None
    contract."""
    data = {"a": {"empty": "", "zero": 0, "flag": False, "lst": []}}
    assert canonical.has(data, "a.empty") is True
    assert canonical.has(data, "a.zero") is True
    assert canonical.has(data, "a.flag") is True
    assert canonical.has(data, "a.lst") is True
