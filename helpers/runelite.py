import win32gui


class Runelite:
    def __enum_window_callback(self, hwnd, _):
        window_text = win32gui.GetWindowText(hwnd)
        if "RuneLite" in window_text:
            x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
            self.rl_window = {
                "x": x0,
                "y": y0,
                "w": x1 - x0,
                "h": y1 - y0,
            }
            self.rl_hwnd = hwnd
            return

    def __find_window(self):
        win32gui.EnumWindows(self.__enum_window_callback, None)
        if not self.rl_hwnd:
            raise Exception("RuneLite window not found.")

    def activate_window(self):
        self.__find_window()
        win32gui.SetForegroundWindow(self.rl_hwnd)
