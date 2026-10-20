"""Godmode plugin: pins player health to max each tick."""
from __future__ import annotations

from src.core.contracts import TrainerContext


class GodModePlugin:
    NAME = "godmode"
    VERSION = "1.2.0"
    REQUIRES: list[str] = []

    def enable(self, ctx: TrainerContext) -> None:
        self._health = ctx.offsets.get("health")
        self._max = ctx.offsets.get("max_health")
        self._base = ctx.state["backend"].base

    def tick(self, ctx: TrainerContext) -> None:
        be = ctx.state["backend"]
        addr = be.resolve_pointer(self._base, self._health)
        max_addr = be.resolve_pointer(self._base, self._max)
        max_hp = be.read_float(max_addr)
        if max_hp > 0:
            be.write_float(addr, max_hp)

    def disable(self, ctx: TrainerContext) -> None:
        pass