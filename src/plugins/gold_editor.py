"""Gold editor — set lunar coins / gold to a target value on hotkey."""
from __future__ import annotations

from src.core.contracts import TrainerContext


class GoldEditorPlugin:
    NAME = "gold_editor"
    VERSION = "1.0.1"
    REQUIRES: list[str] = []
    TARGET_GOLD = 999_999

    def enable(self, ctx: TrainerContext) -> None:
        self._off = ctx.offsets.get("gold")
        self._base = ctx.state["backend"].base
        self._armed = True

    def tick(self, ctx: TrainerContext) -> None:
        if not self._armed:
            return
        be = ctx.state["backend"]
        addr = be.resolve_pointer(self._base, self._off)
        be.write_int(addr, self.TARGET_GOLD)
        self._armed = False

    def disable(self, ctx: TrainerContext) -> None:
        self._armed = False