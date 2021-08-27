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
from munch import munchify, unmunchify


class Window(QWidget):
    interval = 150
    pos = {"x": 0, "y": 0}

    def end_game(message="game is over"):
        print(message)
        sys.exit()

    def update(self):
        if self.pos["x"] < self.settings.cellNum - 1:
            self.pos["x"] += 1
        else:
            self.pos["x"] = 0

        # self.render_point()
        # self.renderMatrixToCheckboxes()

        self.game_loop()

    def game_loop(self):
        ateFood = isEating(self.state.snakeSegments, self.state.food)

        head = self.state.snakeSegments[-1]
        newHead = deepcopy(head)

        d = self.state.snakeDirection
        if (d == "right"):
            if (head["x"] < self.settings.cellNum - 1 or self.settings.checkIsOut):
                newHead["x"] += 1
            else:
                newHead["x"] = 0
        elif (d == "left"):
            if (head["x"] > 0 or self.settings.checkIsOut):
                newHead["x"] -= 1
            else:
                newHead["x"] = self.settings.cellNum - 1
        elif (d == "up"):
            if (head["y"] > 0 or self.settings.checkIsOut):
                newHead["y"] -= 1
            else:
                newHead["y"] = self.settings.cellNum - 1
        if (d == "down"):
            if (head["y"] < self.settings.cellNum - 1 or self.settings.checkIsOut):
                newHead["y"] += 1
            else:
                newHead["y"] = 0

        # del self.state.snakeSegments[0]
        
        if not ateFood:
            # l = len(self.state.snakeSegments)
            self.state.snakeSegments.pop(0)
            # self.state.snakeSegments = unmunchify(self.state.snakeSegments)
            # del self.state.snakeSegments[0]
            # self.state.snakeSegments = munchify(self.state.snakeSegments)
            # l2 = len(self.state.snakeSegments)
            # a = "b"
        else:
            self.state.food = generateFoodPosition(
                self.state.snakeSegments, self.settings.cellNum, self.state.food)
            if not self.state.food:
                self.endGame("You won!")
                return

        self.state.snakeSegments.append(newHead)

        if self.settings.checkIsOut and isOut(self.state.snakeSegments, self.settings.cellNum):
            self.endGame("Snake is out of board. You lost")
            return

        if self.settings.checkIsColliding and isColliding(self.state.snakeSegments):
            self.endGame("Snake collision. You lost")
            return

        matrix = snakeAndFoodToMatrix(self.state.snakeSegments,
                                      self.settings.cellNum, self.state.food)

        matrixToCheckboxes(matrix, self.checkboxes)

        self.state.switchingDirection = False

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
        if self.interval >= 100:
            self.interval -= 50

        self.speedLabel.setText(str(self.interval))

        self.timer.stop()
        self.timer.start(self.interval)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update)

    def speedPlus(self):
        self.interval += 50

        self.speedLabel.setText(str(self.interval))

        self.timer.stop()
        self.timer.start(self.interval)

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

        speedMinus = QAction("interval-", self)
        speedMinus.triggered.connect(self.speedMinus)
        self.toolBar.addAction(speedMinus)

        self.speedLabel = QLabel(str(self.interval))
        self.toolBar.addWidget(self.speedLabel)

        speedPlus = QAction("interval+", self)
        speedPlus.triggered.connect(self.speedPlus)
        self.toolBar.addAction(speedPlus)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.settings = munchify(readWriteSettings())

        snakeSegments = [
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 2, "y": 0},
            {"x": 3, "y": 0},
            {"x": 4, "y": 0},
        ]

        self.state = munchify({
            "snakeDirection": "right",
            # "snakeDirection": "left",
            # "snakeDirection": "down",
            "isPaused": True,
            "snakeSegments": snakeSegments,
            # "food": generateFoodPosition(snakeSegments, self.settings.cellNum),
            "food": Munch(x=5, y=0),
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
        self.timer.start(self.interval)

    def keyPressEvent(self, event):
        allowed_keys = [
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_P,
            1047  # "p" or "з" in russian layout
        ]
        # if event.key() == QtCore.Qt.Key_Q:
        #     print "Killing"
        #     self.deleteLater()
        # elif event.key() == QtCore.Qt.Key_Enter:
        #     self.proceed()
        k = event.key()

        if k in allowed_keys:
            if not self.state.switchingDirection:
                if k == QtCore.Qt.Key_Up:
                    if self.pos["y"] > 0:
                        self.pos["y"] -= 1
                    else:
                        self.pos["y"] = self.settings.cellNum - 1

                    if (
                        self.state.snakeDirection != "up" and
                        self.state.snakeDirection != "down"
                    ):
                        self.state.snakeDirection = "up"
                        self.state.switchingDirection = True

                elif k == QtCore.Qt.Key_Down:
                    if self.pos["y"] < self.settings.cellNum - 1:
                        self.pos["y"] += 1
                    else:
                        self.pos["y"] = 0

                    if (
                        self.state.snakeDirection != "up" and
                        self.state.snakeDirection != "down"
                    ):
                        self.state.snakeDirection = "down"
                        self.state.switchingDirection = True

                elif k == QtCore.Qt.Key_Left:
                    if self.pos["x"] > 0:
                        self.pos["x"] -= 1
                    else:
                        self.pos["x"] = self.settings.cellNum - 1

                    if (
                        self.state.snakeDirection != "right" and
                        self.state.snakeDirection != "left"
                    ):
                        self.state.snakeDirection = "left"
                        self.state.switchingDirection = True

                elif k == QtCore.Qt.Key_Right:
                    if self.pos["x"] < self.settings.cellNum - 1:
                        self.pos["x"] += 1
                    else:
                        self.pos["x"] = 0

                    if (
                        self.state.snakeDirection != "right" and
                        self.state.snakeDirection != "left"
                    ):
                        self.state.snakeDirection = "right"
                        self.state.switchingDirection = True

        # else:
        #     event.accept()
        # print(event.key())


if __name__ == "__main__":
    if not doSettingsExist():
        createSettingsFile()

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
