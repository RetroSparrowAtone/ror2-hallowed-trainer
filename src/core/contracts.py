"""Shared contracts between the trainer host and plugins."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from src.offsets.resolver import OffsetResolver
from src.utils.config import TrainerConfig


@dataclass
class TrainerContext:
    config: TrainerConfig
    offsets: OffsetResolver
    logger: Any
    state: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class TrainerPlugin(Protocol):
    NAME: str
    VERSION: str
    REQUIRES: list[str]

    def enable(self, ctx: TrainerContext) -> None: ...
    def disable(self, ctx: TrainerContext) -> None: ...
    def tick(self, ctx: TrainerContext) -> None: ...


class MemoryBackend(Protocol):
    def read(self, address: int, size: int) -> bytes: ...
    def write(self, address: int, data: bytes) -> None: ...
    def resolve_pointer(self, base: int, offsets: list[int]) -> int: ...