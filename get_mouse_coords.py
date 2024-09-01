import pyautogui
import keyboard
from threading import Thread

# Flag to indicate whether the listener should keep running
running = True


def close_listener():
    global running
    while running:
        if keyboard.is_pressed("esc"):
            print("Exiting...")
            running = False
            break


def get_mouse_position_on_keypress(key="space"):
    """
    Prints the current mouse position when the specified key is pressed.

    :param key: The key that triggers the mouse position capture. Default is 'space'.
    """
    print(f"Press '{key}' to get the mouse position. Press 'esc' to exit.")

    # Start the close listener thread
    listener_thread = Thread(target=close_listener)
    listener_thread.start()

    while running:
        if keyboard.is_pressed(key):
            x, y = pyautogui.position()
            print(f"Mouse position: X={x}, Y={y}")
            keyboard.wait(key)

    listener_thread.join()  # Ensure the listener thread exits cleanly


# Example usage
get_mouse_position_on_keypress("space")
