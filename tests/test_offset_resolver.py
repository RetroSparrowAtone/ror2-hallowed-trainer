from pathlib import Path

import pytest

from src.offsets.resolver import OffsetResolver


class _Cfg:
    local_path = str(Path(__file__).parent.parent / "src/offsets/hallowed_2026.json")


def test_loads_build_string():
    r = OffsetResolver(_Cfg())
    r.load()
    assert "hallowed" in r.build()


def test_get_health_offsets():
    r = OffsetResolver(_Cfg())
    r.load()
    chain = r.get("health")
    assert isinstance(chain, list) and len(chain) >= 2


def test_unknown_offset_raises():
    r = OffsetResolver(_Cfg())
    r.load()
    with pytest.raises(KeyError):
        r.get("does_not_exist")