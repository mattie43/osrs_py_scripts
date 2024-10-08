import sys
import keyboard
from PySide6 import QtWidgets, QtCore
from helpers.runelite import activate_runelite
from helpers.find import find_color, find_image
from helpers.mouse import mouse_move
from helpers.store import colors
from helpers.inventory import click_inv_slot, is_inv_slot_empty


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.__create_script_ddl()
        self.__create_options_ddl()
        # Leave any gap between ddl's and buttons
        self.layout.addStretch()
        self.__create_start_btn()
        self.__create_script_setup_btn()
        self.__create_helper_text()
        self.__create_status_label()

        keyboard.add_hotkey("ctrl+q", self.__stop_curr_script)

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
            "Select script options", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        ddl = QtWidgets.QComboBox()
        ddl.addItems(["None"])
        ddl.activated.connect(handle_change)
        self.layout.addWidget(text)
        self.layout.addWidget(ddl)

    def __create_start_btn(self):
        def start_script():
            activate_runelite()
            self.update_status("starting")
            for x in range(10):
                img = is_inv_slot_empty(x + 1)
                print("img found: ", img)

        button = QtWidgets.QPushButton("Start Script")
        button.clicked.connect(start_script)
        self.layout.addWidget(button)

    def __create_script_setup_btn(self):
        def show_setup():
            print("show setup..")

        button = QtWidgets.QPushButton("Script setup")
        button.clicked.connect(show_setup)
        self.layout.addWidget(button)

    def __create_helper_text(self):
        text = QtWidgets.QLabel(
            "Press ctrl+q to quit the current script.",
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        self.layout.addWidget(text)

    def __create_status_label(self):
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        self.status_label = QtWidgets.QLabel(
            "Script status: Stopped",
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        self.layout.addWidget(divider)
        self.layout.addWidget(self.status_label)

    def __stop_curr_script(self):
        self.update_status("Stopped")
        print("stopping script..")

    def update_status(self, status):
        self.status_label.setText(f"Script status: {status}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = App()
    widget.setWindowTitle("Mattie's Scripts")
    widget.setFixedSize(260, 210)
    widget.show()

    sys.exit(app.exec())
