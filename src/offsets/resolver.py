"""Resolve named offsets for the current Risk of Rain 2 build."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class OffsetResolver:
    def __init__(self, cfg: Any) -> None:
        self.cfg = cfg
        self._table: dict[str, Any] = {}

    def load(self) -> None:
        path = Path(self.cfg.local_path)
        if not path.exists():
            raise FileNotFoundError(f"Offset table missing: {path}")
        self._table = json.loads(path.read_text(encoding="utf-8"))

    def get(self, name: str) -> list[int]:
        entry = self._table.get(name)
        if entry is None:
            raise KeyError(f"Unknown offset '{name}'")
        return list(entry)

    def build(self) -> str:
        return self._table.get("_build", "unknown")