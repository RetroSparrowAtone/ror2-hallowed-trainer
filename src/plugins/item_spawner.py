"""Item spawner — writes item IDs into the player's inventory array."""
from __future__ import annotations

from src.core.contracts import TrainerContext


class ItemSpawnerPlugin:
    NAME = "item_spawner"
    VERSION = "0.4.0"
    REQUIRES = ["godmode"]

    def enable(self, ctx: TrainerContext) -> None:
        self._base = ctx.state["backend"].base
        self._queue: list[int] = []

    def queue_item(self, item_id: int) -> None:
        self._queue.append(item_id)

    def tick(self, ctx: TrainerContext) -> None:
        if not self._queue:
            return
        be = ctx.state["backend"]
        for item_id in self._queue:
            # inventory index is resolved lazily via the player base offset
            addr = be.resolve_pointer(self._base, ctx.offsets.get("player_base"))
            be.write_int(addr + 0x40 + item_id * 4, 1)
        self._queue.clear()

    def disable(self, ctx: TrainerContext) -> None:
        self._queue.clear()