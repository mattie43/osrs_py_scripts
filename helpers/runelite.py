import win32gui
import time
from helpers.store import rl


def __enum_window_callback(hwnd, _):
    window_text = win32gui.GetWindowText(hwnd)
    if "RuneLite" in window_text:
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        rl["window"] = {
            "x": x0,
            "y": y0,
            "w": x1 - x0,
            "h": y1 - y0,
        }
        rl["hwnd"] = hwnd
        return


def __find_window():
    win32gui.EnumWindows(__enum_window_callback, None)
    if not rl["hwnd"]:
        raise Exception("RuneLite window not found.")


def activate_runelite():
    __find_window()
    win32gui.SetForegroundWindow(rl["hwnd"])
    time.sleep(0.5)
