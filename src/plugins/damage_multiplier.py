"""Damage multiplier — scales outgoing damage by a configurable factor."""
from __future__ import annotations

from src.core.contracts import TrainerContext


class DamageMultiplierPlugin:
    NAME = "damage_multiplier"
    VERSION = "0.9.3"
    REQUIRES = ["godmode"]
    FACTOR = 5.0

    def enable(self, ctx: TrainerContext) -> None:
        self._off = ctx.offsets.get("damage_mult")
        self._base = ctx.state["backend"].base

    def tick(self, ctx: TrainerContext) -> None:
        be = ctx.state["backend"]
        addr = be.resolve_pointer(self._base, self._off)
        be.write_float(addr, self.FACTOR)

    def disable(self, ctx: TrainerContext) -> None:
        be = ctx.state["backend"]
        addr = be.resolve_pointer(self._base, self._off)
        be.write_float(addr, 1.0)