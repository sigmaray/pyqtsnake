# from PyQt5.QtWidgets import (
#     QApplication,
#     QPushButton,
#     QVBoxLayout,
#     QHBoxLayout,
#     QWidget,
#     QCheckBox
# )

from copy import deepcopy
import sys
from PyQt5 import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from constants import *
from lib import *
from munch import munchify


class Window(QWidget):
    speed = 150
    pos = {"x": 0, "y": 0}

    def update(self):
        if self.pos["x"] < self.settings.cellNum - 1:
            self.pos["x"] += 1
        else:
            self.pos["x"] = 0

        self.render_point()
        # self.renderMatrixToCheckboxes()
        matrix = snakeAndFoodToMatrix(self.state.snakeSegments,
                                      self.settings.cellNum, self.state.food)

        matrixToCheckboxes(matrix, self.checkboxes)

    def game_loop(self):
        ateFood = isEating(self.state.snakeSegments, self.state.food)

        head = self.state.snakeSegments[-1]
        newHead = deepcopy(head)

    def render_point(self):
        # for row in self.checkboxes:
        for y, row in enumerate(self.checkboxes):
            for x, c in enumerate(row):
                # [self.pos["y"]][self.pos["x"]]
                if y == self.pos["y"] and x == self.pos["x"]:
                    c.setEnabled(True)
                    c.setChecked(True)
                else:
                    c.setChecked(False)
                    c.setEnabled(False)

    def speedMinus(self):
        if self.speed >= 100:
            self.speed -= 50

        self.speedLabel.setText(str(self.speed))

        self.timer.stop()
        self.timer.start(self.speed)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update)

    def speedPlus(self):
        self.speed += 50

        self.speedLabel.setText(str(self.speed))

        self.timer.stop()
        self.timer.start(self.speed)

    def add_toolbar(self):
        # Create pyqt toolbar
        self.toolBar = QToolBar()
        self.layout.addWidget(self.toolBar)

        # # Add buttons to toolbar
        # toolButton = QToolButton()
        # toolButton.setText("Apple")
        # toolButton.setCheckable(True)
        # # toolButton.setAutoExclusive(True)
        # toolBar.addWidget(toolButton)
        # toolButton = QToolButton()
        # toolButton.setText("Orange")
        # toolButton.setCheckable(True)
        # # toolButton.setAutoExclusive(True)
        # toolBar.addWidget(toolButton)

        speedMinus = QAction("speed-", self)
        speedMinus.triggered.connect(self.speedMinus)
        self.toolBar.addAction(speedMinus)

        self.speedLabel = QLabel(str(self.speed))
        self.toolBar.addWidget(self.speedLabel)

        speedPlus = QAction("speed+", self)
        speedPlus.triggered.connect(self.speedPlus)
        self.toolBar.addAction(speedPlus)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.settings = munchify(readWriteSettings())
        print(self.settings)

        snakeSegments = [
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 2, "y": 0},
            {"x": 3, "y": 0},
            {"x": 4, "y": 0},
        ]

        self.state = munchify({
            "snakeDirection": "right",
            "isPaused": True,
            "snakeSegments": snakeSegments,
            "food": generateFoodPosition(snakeSegments, self.settings.cellNum),
            "switchingDirection": False,
        })

        self.add_toolbar()

        self.checkboxes = []
        for _ in range(self.settings.cellNum):
            row = []
            # vl = QVBoxLayout()
            hl = QHBoxLayout()

            for _ in range(self.settings.cellNum):
                c = QCheckBox()
                c.setEnabled(False)
                c.setStyleSheet(genStyleSheet(COLORS.canvasColor))
                hl.addWidget(c)
                row.append(c)

            self.checkboxes.append(row)
            self.layout.addLayout(hl)

        # Set the layout on the application's window
        self.setLayout(self.layout)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(self.speed)

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

        if k in allowed_keys:
            if k == QtCore.Qt.Key_Up:
                if self.pos["y"] > 0:
                    self.pos["y"] -= 1
                else:
                    self.pos["y"] = self.settings.cellNum - 1
            elif k == QtCore.Qt.Key_Down:
                if self.pos["y"] < self.settings.cellNum - 1:
                    self.pos["y"] += 1
                else:
                    self.pos["y"] = 0
            elif k == QtCore.Qt.Key_Left:
                if self.pos["x"] > 0:
                    self.pos["x"] -= 1
                else:
                    self.pos["x"] = self.settings.cellNum - 1
            elif k == QtCore.Qt.Key_Right:
                if self.pos["x"] < self.settings.cellNum - 1:
                    self.pos["x"] += 1
                else:
                    self.pos["x"] = 0

        else:
            event.accept()
        # print(event.key())


if __name__ == "__main__":
    if not doSettingsExist():
        createSettingsFile()

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
