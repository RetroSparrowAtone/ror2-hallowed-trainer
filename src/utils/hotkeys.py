"""Win32 hotkey polling for toggle / panic keys."""
from __future__ import annotations

import ctypes

VK_MAP = {
    "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73,
    "F5": 0x74, "F6": 0x75, "F7": 0x76, "F8": 0x77,
    "F9": 0x78, "F10": 0x79, "F11": 0x7A, "F12": 0x7B,
    "END": 0x23, "HOME": 0x24, "INSERT": 0x2D,
}


class HotkeyWatcher:
    def __init__(self, toggle: str, panic: str) -> None:
        self._toggle_vk = VK_MAP.get(toggle.upper(), 0x77)
        self._panic_vk = VK_MAP.get(panic.upper(), 0x23)
        self._user32 = ctypes.windll.user32

    def _down(self, vk: int) -> bool:
        return bool(self._user32.GetAsyncKeyState(vk) & 0x8000)

    def toggle_pressed(self) -> bool:
        return self._down(self._toggle_vk)

    def panic_pressed(self) -> bool:
        return self._down(self._panic_vk)