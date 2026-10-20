"""Static registry used by tooling and tests to enumerate bundled plugins."""
from src.plugins import (
    damage_multiplier,
    godmode,
    gold_editor,
    item_spawner,
    teleporter_esp,
)

PLUGINS = [
    godmode.GodModePlugin,
    damage_multiplier.DamageMultiplierPlugin,
    item_spawner.ItemSpawnerPlugin,
    gold_editor.GoldEditorPlugin,
    teleporter_esp.TeleporterEspPlugin,
]

__all__ = ["PLUGINS"]