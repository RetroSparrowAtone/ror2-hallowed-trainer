"""Discovers and wires TrainerPlugin subclasses."""
from __future__ import annotations

import importlib
import inspect
import pkgutil
from typing import Iterable

from src.core.contracts import TrainerContext, TrainerPlugin
from src.core.host import TrainerHost


class PluginLoader:
    def __init__(self, host: TrainerHost, cfg) -> None:
        self.host = host
        self.cfg = cfg
        self._plugins: dict[str, TrainerPlugin] = {}

    def discover(self, package: str) -> None:
        pkg = importlib.import_module(package)
        for mod_info in pkgutil.iter_modules(pkg.__path__):
            module = importlib.import_module(f"{package}.{mod_info.name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if obj is TrainerPlugin or not issubclass(obj, object):
                    continue
                if getattr(obj, "NAME", None) and hasattr(obj, "enable"):
                    self._plugins[obj.NAME] = obj()

    def _resolve_deps(self) -> Iterable[TrainerPlugin]:
        seen: set[str] = set()
        out: list[TrainerPlugin] = []
        def visit(name: str) -> None:
            if name in seen:
                return
            plugin = self._plugins[name]
            for dep in getattr(plugin, "REQUIRES", []):
                if dep in self._plugins:
                    visit(dep)
            seen.add(name)
            out.append(plugin)
        for name in self._plugins:
            visit(name)
        return out

    def enable_all(self) -> None:
        enabled = set(self.cfg.enabled)
        active = []
        for plugin in self._resolve_deps():
            if plugin.NAME not in enabled:
                continue
            try:
                plugin.enable(self.host.ctx)
                active.append(plugin)
                self.host.log.info("Enabled plugin %s v%s", plugin.NAME, plugin.VERSION)
            except Exception as exc:  # noqa: BLE001
                self.host.log.exception("Failed to enable %s: %s", plugin.NAME, exc)
        self.host.ctx.state["active_plugins"] = active

    def disable_all(self) -> None:
        for plugin in self.host.ctx.state.get("active_plugins", []):
            try:
                plugin.disable(self.host.ctx)
            except Exception as exc:  # noqa: BLE001
                self.host.log.exception("Disable error %s: %s", plugin.NAME, exc)