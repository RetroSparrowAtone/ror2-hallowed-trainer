"""Config loader with strict typing via dataclasses."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class GameConfig:
    exe_path: str
    process_name: str
    module_name: str


@dataclass
class TrainerSettings:
    hotkey_toggle: str
    hotkey_panic: str
    log_level: str = "INFO"
    auto_attach: bool = True


@dataclass
class PluginConfig:
    enabled: list[str] = field(default_factory=list)
    disabled: list[str] = field(default_factory=list)


@dataclass
class OffsetConfig:
    source: str
    local_path: str


@dataclass
class TrainerConfig:
    game: GameConfig
    trainer: TrainerSettings
    plugins: PluginConfig
    offsets: OffsetConfig


def load_config(path: str | Path) -> TrainerConfig:
    data: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return TrainerConfig(
        game=GameConfig(**data["game"]),
        trainer=TrainerSettings(**data["trainer"]),
        plugins=PluginConfig(**data["plugins"]),
        offsets=OffsetConfig(**data["offsets"]),
    )