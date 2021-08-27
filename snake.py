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

LABEL_PLACEHOLDER = " "


class Window(QWidget):
    def generateState(self):
        snakeSegments = [
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 2, "y": 0},
            {"x": 3, "y": 0},
            {"x": 4, "y": 0},
        ]

        return munchify({
            "snakeDirection": "right",
            # "snakeDirection": "left",
            # "snakeDirection": "down",
            "isPaused": False,
            "snakeSegments": snakeSegments,
            "food": generateFoodPosition(snakeSegments, self.settings.cellNum),
            # "food": Munch(x=5, y=0),
            "switchingDirection": False,
        })

    def restart(self):
        self.state = self.generateState()
        self.labelStatus.setText(LABEL_PLACEHOLDER)
        self.timer.start(self.settings.intervalMilliseconds)

    def pauseUnpause(self):
        if not self.state.isPaused:
            self.state.isPaused = True
            # clearInterval(interval);
            self.timer.stop()
            self.labelStatus.setText("paused")
        else:
            self.state.isPaused = False
            self.timer.start(self.settings.intervalMilliseconds)
            self.labelStatus.setText(LABEL_PLACEHOLDER)

    def endGame(self, message="game is over"):
        # print(message)
        self.labelStatus.setText(message)
        self.timer.stop()
        # sys.exit()

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

        if not ateFood:
            self.state.snakeSegments.pop(0)
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

    def decreaseInterval(self):
        if self.settings.intervalMilliseconds >= 100:
            self.settings.intervalMilliseconds -= 50

        writeSettingsFile(unmunchify(self.settings))

        self.speedLabel.setText(str(self.settings.intervalMilliseconds))

        self.timer.stop()
        self.timer.start(self.settings.intervalMilliseconds)

    def increaseInterval(self):
        self.settings.intervalMilliseconds += 50

        writeSettingsFile(unmunchify(self.settings))

        self.speedLabel.setText(str(self.settings.intervalMilliseconds))

        self.timer.stop()
        self.timer.start(self.settings.intervalMilliseconds)

    def add_toolbar(self):
        # Create pyqt toolbar

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

        self.toolBar = QToolBar()
        self.layout.addWidget(self.toolBar)

        actionPauseUnpause = QAction("interval-", self)
        actionPauseUnpause.triggered.connect(self.decreaseInterval)
        self.toolBar.addAction(actionPauseUnpause)

        self.speedLabel = QLabel(str(self.settings.intervalMilliseconds))
        self.toolBar.addWidget(self.speedLabel)

        actionIntervalPlus = QAction("interval+", self)
        actionIntervalPlus.triggered.connect(self.increaseInterval)
        self.toolBar.addAction(actionIntervalPlus)

        actionPauseUnpause = QAction("(un)pause", self)
        actionPauseUnpause.triggered.connect(self.pauseUnpause)
        self.toolBar.addAction(actionPauseUnpause)

        actionRestart = QAction("restart", self)
        actionRestart.triggered.connect(self.restart)
        self.toolBar.addAction(actionRestart)

        self.toolBar2 = QToolBar()
        self.layout.addWidget(self.toolBar2)

        self.labelStatus = QLabel(LABEL_PLACEHOLDER)
        self.toolBar2.addWidget(self.labelStatus)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.settings = munchify(readWriteSettings())

        self.state = self.generateState()

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
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(self.settings.intervalMilliseconds)

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
            if event.key() == QtCore.Qt.Key_P or event.key() == 1047:
                self.pauseUnpause()
            else:
                if not self.state.switchingDirection and not self.state.isPaused:
                    if k == QtCore.Qt.Key_Up:
                        if (
                            self.state.snakeDirection != "up" and
                            self.state.snakeDirection != "down"
                        ):
                            self.state.snakeDirection = "up"
                            self.state.switchingDirection = True

                    elif k == QtCore.Qt.Key_Down:
                        if (
                            self.state.snakeDirection != "up" and
                            self.state.snakeDirection != "down"
                        ):
                            self.state.snakeDirection = "down"
                            self.state.switchingDirection = True

                    elif k == QtCore.Qt.Key_Left:
                        if (
                            self.state.snakeDirection != "right" and
                            self.state.snakeDirection != "left"
                        ):
                            self.state.snakeDirection = "left"
                            self.state.switchingDirection = True

                    elif k == QtCore.Qt.Key_Right:
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
        writeSettingsFile()

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
