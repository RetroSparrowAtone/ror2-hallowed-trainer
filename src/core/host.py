"""Trainer host: owns the memory backend and drives plugin ticks."""
from __future__ import annotations

import time
from typing import Optional

from src.core.contracts import TrainerContext
from src.memory.pymem_backend import PymemBackend
from src.utils.hotkeys import HotkeyWatcher


class TrainerHost:
    def __init__(self, ctx: TrainerContext) -> None:
        self.ctx = ctx
        self.log = ctx.logger
        self.backend: Optional[PymemBackend] = None
        self._running = False
        self._hotkeys = HotkeyWatcher(
            toggle=ctx.config.trainer.hotkey_toggle,
            panic=ctx.config.trainer.hotkey_panic,
        )

    def attach(self) -> bool:
        try:
            self.backend = PymemBackend(self.ctx.config.game.process_name)
            self.ctx.state["backend"] = self.backend
            self.log.info("Attached to %s", self.ctx.config.game.process_name)
            return True
        except Exception as exc:  # noqa: BLE001
            self.log.error("Attach failed: %s", exc)
            return False

    def run_loop(self) -> None:
        if not self.attach():
            self.log.error("Could not attach; aborting")
            return
        self._running = True
        while self._running:
            if self._hotkeys.panic_pressed():
                self.log.warning("Panic hotkey — stopping")
                break
            for plugin in self.ctx.state.get("active_plugins", []):
                try:
                    plugin.tick(self.ctx)
                except Exception as exc:  # noqa: BLE001
                    self.log.exception("Plugin %s tick error: %s", plugin.NAME, exc)
            time.sleep(0.05)

    def shutdown(self) -> None:
        self._running = False
        if self.backend:
            self.backend.close()