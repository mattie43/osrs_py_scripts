import pyautogui
import keyboard


def get_mouse_position():
    print("Press 'space' to get the mouse position. Press 'esc' to exit.")

    def print_coords():
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})")

    keyboard.add_hotkey("space", print_coords)
    keyboard.wait("esc")


get_mouse_position()
