import sys
import keyboard
import threading
import time
from PySide6 import QtWidgets, QtCore
from helpers.index import HelpersIndex


class App(QtWidgets.QWidget, HelpersIndex):
    def __init__(self):
        super().__init__()

        self.ignored_keys = ["space", "tab", "enter", "shift", "ctrl", "alt", "esc"]
        self.hotkey = None
        self.layout = QtWidgets.QVBoxLayout(self)

        self.__create_script_ddl()
        self.__create_options_ddl()
        # Leave any gap between ddl's and buttons
        self.layout.addStretch()
        self.__create_hotkey_btn()
        self.__create_script_setup_btn()

    def __create_script_ddl(self):
        def handle_change(text):
            print(text)

        text = QtWidgets.QLabel(
            "Select script", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        ddl = QtWidgets.QComboBox()
        ddl.addItems(["None"])
        ddl.activated.connect(handle_change)
        self.layout.addWidget(text)
        self.layout.addWidget(ddl)

    def __create_options_ddl(self):
        def handle_change(text):
            print(text)

        text = QtWidgets.QLabel(
            "Script options", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        ddl = QtWidgets.QComboBox()
        ddl.addItems(["None"])
        ddl.activated.connect(handle_change)
        self.layout.addWidget(text)
        self.layout.addWidget(ddl)

    def __create_hotkey_btn(self):
        def click_listener(button):
            self.__update_button_text(button, "...")
            threading.Thread(
                target=self.__wait_for_key, args=(button,), daemon=True
            ).start()

        button = QtWidgets.QPushButton("Set hotkey..")
        button.clicked.connect(lambda: click_listener(button))
        self.layout.addWidget(button)

    def __wait_for_key(self, button):
        keyboard.block_key("space")
        event = keyboard.read_event()
        if (
            event.event_type == keyboard.KEY_DOWN
            and event.name not in self.ignored_keys
        ):
            self.hotkey = event.name
            self.__update_button_text(button, event.name.capitalize())
        else:
            self.hotkey = None
            self.__update_button_text(button, "Set hotkey..")

        keyboard.unblock_key("space")

    def __update_button_text(self, button, text):
        button.setText(text)

    def __create_script_setup_btn(self):
        def click_listener():
            # show setup
            print("show setup..")
            self.activate_window()
            time.sleep(1)
            # center = self.find_image_in("inventory.png")
            # self.mouse_move(center["center_x"], center["center_y"])
            for x in range(10):
                time.sleep(0.05)
                self.select_tab("magic")

        button = QtWidgets.QPushButton("Script setup")
        button.clicked.connect(
            lambda: threading.Thread(target=click_listener()).start()
        )
        self.layout.addWidget(button)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = App()
    widget.setWindowTitle("Mattie's Scripts")
    widget.setFixedSize(260, 200)
    widget.show()

    sys.exit(app.exec())
