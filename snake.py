import sys

from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QCheckBox
)

from PyQt5.QtCore import (
    QTimer
)

from constants import *
from lib import *

from PyQt5 import *

BOARD_SIZE = 20
pos = {"x": 0, "y": 0}

snakeSegments = [
    {"x": 0, "y": 0},
    {"x": 1, "y": 0},
    {"x": 2, "y": 0},
    {"x": 3, "y": 0},
    {"x": 4, "y": 0},
]

state = {
    "snakeDirection": "right",
    "isPaused": True,
    "snakeSegments": snakeSegments,
    "food": generateFoodPosition(snakeSegments, DEFAULT_SETTINGS["cellNum"]),
    "switchingDirection": False,
}


class Window(QWidget):

    def update(self):
        if pos["x"] < DEFAULT_SETTINGS["cellNum"] - 1:
            pos["x"] += 1
        else:
            pos["x"] = 0

        # print(pos)
        # print("l29")
        self.render_point()

    def render_point(self):
        # for row in self.checkboxes:
        for y, row in enumerate(self.checkboxes):
            for x, c in enumerate(row):
                # [pos["y"]][pos["x"]]
                # print([y,x])
                if y == pos["y"] and x == pos["x"]:
                    c.setEnabled(True)
                    c.setChecked(True)
                else:
                    c.setChecked(False)
                    c.setEnabled(False)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.checkboxes = []
        for _ in range(DEFAULT_SETTINGS["cellNum"]):
            row = []
            # vl = QVBoxLayout()
            hl = QHBoxLayout()

            for _ in range(DEFAULT_SETTINGS["cellNum"]):
                c = QCheckBox()
                c.setEnabled(False)
                hl.addWidget(c)
                row.append(c)

            self.checkboxes.append(row)
            layout.addLayout(hl)

        # Set the layout on the application's window
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(100)

    def keyPressEvent(self, event):
        allowed_keys = [
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_P,
            1047  # P in russian keyboard layout
        ]
        # if event.key() == QtCore.Qt.Key_Q:
        #     print "Killing"
        #     self.deleteLater()
        # elif event.key() == QtCore.Qt.Key_Enter:
        #     self.proceed()
        k = event.key()
        print(k)
        if k in allowed_keys:
            print("allowed")

            if k == QtCore.Qt.Key_Up:
                if pos["y"] > 0:
                    pos["y"] -= 1
                else:
                    pos["y"] = DEFAULT_SETTINGS["cellNum"] - 1
            elif k == QtCore.Qt.Key_Down:
                if pos["y"] < DEFAULT_SETTINGS["cellNum"] - 1:
                    pos["y"] += 1
                else:
                    pos["y"] = 0

            print(pos)
        else:
            event.accept()
        # print(event.key())


print(COLORS)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
