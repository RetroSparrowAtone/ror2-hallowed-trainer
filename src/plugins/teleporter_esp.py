"""Teleporter ESP — logs teleporter world positions to the console."""
from __future__ import annotations

from src.core.contracts import TrainerContext


class TeleporterEspPlugin:
    NAME = "teleporter_esp"
    VERSION = "0.2.1"
    REQUIRES: list[str] = []

    def enable(self, ctx: TrainerContext) -> None:
        self._off = ctx.offsets.get("teleporter_list")
        self._base = ctx.state["backend"].base
        self._seen: set[int] = set()

    def tick(self, ctx: TrainerContext) -> None:
        be = ctx.state["backend"]
        head = be.resolve_pointer(self._base, self._off)
        count = be.read_int(head)
        if count <= 0 or count > 64:
            return
        for i in range(count):
            ptr = be.read_int(head + 0x8 + i * 8)
            if ptr and ptr not in self._seen:
                self._seen.add(ptr)
                ctx.logger.info("[ESP] teleporter @ 0x%X", ptr)

    def disable(self, ctx: TrainerContext) -> None:
        self._seen.clear()