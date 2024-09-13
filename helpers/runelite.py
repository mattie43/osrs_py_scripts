import win32gui
import time
from helpers.store import store


def __enum_window_callback(hwnd, _):
    window_text = win32gui.GetWindowText(hwnd)
    if "RuneLite" in window_text:
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        store["rl"]["window"] = {
            "x": x0,
            "y": y0,
            "w": x1 - x0,
            "h": y1 - y0,
        }
        store["rl"]["hwnd"] = hwnd
        return


def __find_window():
    win32gui.EnumWindows(__enum_window_callback, None)
    if not store["rl"]["hwnd"]:
        raise Exception("RuneLite window not found.")


def activate_runelite():
    __find_window()
    win32gui.SetForegroundWindow(store["rl"]["hwnd"])
    time.sleep(0.5)
