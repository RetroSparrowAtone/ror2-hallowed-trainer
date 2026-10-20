"""Thin wrapper around pymem for Risk of Rain 2 memory IO."""
from __future__ import annotations

import struct

from pymem import Pymem
from pymem.process import module_from_name


class PymemBackend:
    def __init__(self, process_name: str) -> None:
        self.pm = Pymem(process_name)
        self.base = module_from_name(self.pm.process_handle, "GameAssembly.dll").lpBaseOfDll

    def read(self, address: int, size: int) -> bytes:
        return self.pm.read_bytes(address, size)

    def write(self, address: int, data: bytes) -> None:
        self.pm.write_bytes(address, data, len(data))

    def read_int(self, address: int) -> int:
        return struct.unpack("<i", self.read(address, 4))[0]

    def write_int(self, address: int, value: int) -> None:
        self.write(address, struct.pack("<i", value))

    def read_float(self, address: int) -> float:
        return struct.unpack("<f", self.read(address, 4))[0]

    def write_float(self, address: int, value: float) -> None:
        self.write(address, struct.pack("<f", value))

    def resolve_pointer(self, base: int, offsets: list[int]) -> int:
        addr = base
        for off in offsets[:-1]:
            addr = self.read_int(addr + off)
        return addr + offsets[-1]

    def close(self) -> None:
        try:
            self.pm.close_process()
        except Exception:
            pass