"""Utility: dump candidate offsets from a live Risk of Rain 2 process."""
from __future__ import annotations

import argparse
import json

from src.memory.pymem_backend import PymemBackend


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", default="Risk of Rain 2.exe")
    ap.add_argument("--out", default="offsets/dump.json")
    args = ap.parse_args()

    be = PymemBackend(args.process)
    print(f"base=0x{be.base:X}")
    # crude scan: read 4KB around the player base pointer
    blob = be.read(be.base + 0x1A3F2C0, 0x1000)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump({"base": be.base, "size": len(blob)}, fh, indent=2)
    be.close()


if __name__ == "__main__":
    main()
</final>