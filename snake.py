"""Snake game with checkboxes"""
from copy import deepcopy
import sys
from typing import Literal, List
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QToolBar, QAction,
                             QLabel, QHBoxLayout, QCheckBox)
from munch import Munch
from settings_dialog import SettingsDialog
import lib
import constants
import type_declarations as t


class SnakeCheckboxes(QWidget):
    """PyQt window"""

    # Add some content to prevent form elements moving
    LABEL_PLACEHOLDER = " "

    state: t.State

    # Put all widgets inside the scope
    widgets = Munch()

    def __init__(self):
        super().__init__()

        if not lib.doSettingsExist():
            lib.writeSettingsFile(constants.DEFAULT_SETTINGS)

        self.widgets.layout = QVBoxLayout()

        self.settings = lib.readOrCreateSettings()

        self.state = self.generateState()

        self.addToolbar()

        self.addBoard()

        self.setLayout(self.widgets.layout)

        self.addTimer()

    def addTimer(self):
        """Add timer and connect it to handler function"""
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(self.settings.intervalMilliseconds)

    def generateState(self):
        """Generate initial game state"""
        snakeSegments = [
            t.Coordinate(x=0, y=0)
        ]

        return t.State(
            snakeDirection="right",
            isPaused=False,
            snakeSegments=snakeSegments,
            food=lib.generateFoodPosition(
                snakeSegments, self.settings.cellNum),
            switchingDirection=False,
        )

    def onClickRestart(self):
        """When Restart button is clicked: restart the game"""
        self.state = self.generateState()
        self.widgets.labelStatus.setText(self.LABEL_PLACEHOLDER)
        self.timer.start(self.settings.intervalMilliseconds)

    def pause(self):
        """Pause the game"""
        self.state.isPaused = True
        self.timer.stop()
        self.widgets.labelStatus.setText("paused")

    def unpause(self):
        """Unpause the game"""
        self.state.isPaused = False
        self.timer.start(self.settings.intervalMilliseconds)
        self.widgets.labelStatus.setText(self.LABEL_PLACEHOLDER)

    def onTogglePauseClick(self):
        """When user clicked on Pause or Unpause button"""
        if not self.state.isPaused:
            self.state.isPaused = True
            self.timer.stop()
            self.widgets.labelStatus.setText("paused")
        else:
            self.state.isPaused = False
            self.timer.start(self.settings.intervalMilliseconds)
            self.widgets.labelStatus.setText(self.LABEL_PLACEHOLDER)

    def endGame(self, message: str = "game is over"):
        """
        End the game:
        * Show a message to user
        * Stop timer
        """
        self.widgets.labelStatus.setText(message)
        self.timer.stop()

    def onTimer(self):
        """When timer is triggerd: do next iteration of the game"""
        self.makeMove()

    def makeMove(self):
        """
        When timer is called or when user presses same button a few times:
        * Move snake by one cell
        * Check if food is eaten (generate new random food and increase snake lenght)
        * Check if game is over
        * Call renderer
        """
        ateFood = lib.isEating(self.state.snakeSegments, self.state.food)

        oldHead = self.state.snakeSegments[-1]
        newHead = deepcopy(oldHead)

        snakeDirection = self.state.snakeDirection
        if snakeDirection == "right":
            if (oldHead.x < self.settings.cellNum - 1 or self.settings.checkIsOut):
                newHead.x += 1
            else:
                newHead.x = 0
        elif snakeDirection == "left":
            if (oldHead.x > 0 or self.settings.checkIsOut):
                newHead.x -= 1
            else:
                newHead.x = self.settings.cellNum - 1
        elif snakeDirection == "up":
            if (oldHead.y > 0 or self.settings.checkIsOut):
                newHead.y -= 1
            else:
                newHead.y = self.settings.cellNum - 1
        if snakeDirection == "down":
            if (oldHead.y < self.settings.cellNum - 1 or self.settings.checkIsOut):
                newHead.y += 1
            else:
                newHead.y = 0

        if not ateFood:
            self.state.snakeSegments.pop(0)
        else:
            self.state.food = lib.generateFoodPosition(
                self.state.snakeSegments, self.settings.cellNum)
            if not self.state.food:
                self.endGame("You won!")
                return

        self.state.snakeSegments.append(newHead)

        if self.settings.checkIsOut and lib.isOut(self.state.snakeSegments, self.settings.cellNum):
            self.endGame("Snake is out of board. You lost")
            return

        if self.settings.checkIsColliding and lib.isColliding(self.state.snakeSegments):
            self.endGame("Snake collision. You lost")
            return

        matrix = lib.snakeAndFoodToMatrix(self.state.snakeSegments,
                                          self.settings.cellNum, self.state.food)

        self.render(matrix)

        self.state.switchingDirection = False

    def determineDelta(self, currentInterval: int, direction: Literal["up", "down"]):
        """
        Determine how fast to change the interval (when user clicks button).
        If interval is small and change it slower.
        If it is large change it faster.
        """
        if 20 <= currentInterval <= 250:
            delta = 10
        elif 10 < currentInterval < 20:
            if direction == "down":
                delta = currentInterval - 10
            elif direction == "up":
                delta = 20 - currentInterval
        elif currentInterval == 10:
            if direction == "down":
                delta = 1
            elif direction == "up":
                delta = 10
        elif 0 < currentInterval < 10:
            delta = 1
        elif currentInterval == 0:
            if direction == "down":
                delta = 0
            elif direction == "up":
                delta = 1
        else:
            delta = 50
        return delta

    def onIntervalDecrClick(self):
        """Speed up snake (when user clicks UI button or presses PageDown)"""
        self.settings.intervalMilliseconds -= self.determineDelta(
            self.settings.intervalMilliseconds, "down")

        lib.writeSettingsFile(self.settings)

        self.widgets.speedLabel.setText(
            str(self.settings.intervalMilliseconds))

        self.timer.stop()
        self.timer.start(self.settings.intervalMilliseconds)

    def onIntervalIncrClick(self):
        """Slow down snake (when user clicks UI button or presses PageUp"""
        self.settings.intervalMilliseconds += self.determineDelta(
            self.settings.intervalMilliseconds, "up")

        lib.writeSettingsFile(self.settings)

        self.widgets.speedLabel.setText(
            str(self.settings.intervalMilliseconds))

        self.timer.stop()
        self.timer.start(self.settings.intervalMilliseconds)

    def onShowSettingsClick(self):
        """When user clicks Settings button"""
        self.pause()
        settings, result = SettingsDialog.run(self.settings)
        if result:
            lib.writeSettingsFile(settings)

            # https://stackoverflow.com/a/62611055
            QtCore.QCoreApplication.quit()
            QtCore.QProcess.startDetached(sys.executable, sys.argv)
        else:
            self.unpause()

    def addToolbar(self):
        """Add toolbars with control buttons, bind buttons to click handlers"""
        self.widgets.toolBar = QToolBar()
        self.widgets.layout.addWidget(self.widgets.toolBar)

        actionPauseUnpause = QAction("interval-", self)
        actionPauseUnpause.triggered.connect(self.onIntervalDecrClick)
        self.widgets.toolBar.addAction(actionPauseUnpause)

        self.widgets.speedLabel = QLabel(
            str(self.settings.intervalMilliseconds))
        self.widgets.toolBar.addWidget(self.widgets.speedLabel)

        actionIntervalPlus = QAction("interval+", self)
        actionIntervalPlus.triggered.connect(self.onIntervalIncrClick)
        self.widgets.toolBar.addAction(actionIntervalPlus)

        self.widgets.toolBar2 = QToolBar()
        self.widgets.layout.addWidget(self.widgets.toolBar2)

        actionPauseUnpause = QAction("(un)pause", self)
        actionPauseUnpause.triggered.connect(self.onTogglePauseClick)
        self.widgets.toolBar2.addAction(actionPauseUnpause)

        actionRestart = QAction("restart", self)
        actionRestart.triggered.connect(self.onClickRestart)
        self.widgets.toolBar2.addAction(actionRestart)

        actionSettings = QAction("settings", self)
        actionSettings.triggered.connect(self.onShowSettingsClick)
        self.widgets.toolBar2.addAction(actionSettings)

        self.widgets.toolBar3 = QToolBar()
        self.widgets.layout.addWidget(self.widgets.toolBar3)

        self.widgets.labelStatus = QLabel(self.LABEL_PLACEHOLDER)
        self.widgets.toolBar3.addWidget(self.widgets.labelStatus)

    def render(self, matrix: List[List[t.CellType]]):
        """Render 2D array to checkboxes"""
        lib.matrixToCheckboxes(matrix, self.widgets.checkboxes)

    def addBoard(self):
        """
        Add board that will contain snake and food:
        Create layout and checkboxes
        """
        self.widgets.checkboxes = []
        for _ in range(self.settings.cellNum):
            row = []

            hl = QHBoxLayout()

            for _ in range(self.settings.cellNum):
                c = QCheckBox()
                c.setEnabled(False)
                hl.addWidget(c)
                row.append(c)

            self.widgets.checkboxes.append(row)
            self.widgets.layout.addLayout(hl)

    def keyPressEvent(self, event):
        """
        When user presses keyboard button:
        * Change direction (if user pressesed different button)
        * Move snake faster (when user presses same button one more time)
        * Pause/unpase (when user clicked P button)
        * Increase speed (when user presses PageDown)
        * Decrease speed (when user presses PageUp)
        """
        allowedKeys = [
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_P,
            1047,  # "p" in russian layout
            QtCore.Qt.Key_PageUp,
            QtCore.Qt.Key_PageDown
        ]

        k = event.key()

        if k in allowedKeys:
            if event.key() == QtCore.Qt.Key_P or event.key() == 1047:
                self.onTogglePauseClick()
            elif event.key() == QtCore.Qt.Key_PageUp:
                self.onIntervalIncrClick()
            elif event.key() == QtCore.Qt.Key_PageDown:
                self.onIntervalDecrClick()
            else:
                toSpeedUp = False
                if not self.state.switchingDirection and not self.state.isPaused:
                    if k == QtCore.Qt.Key_Up:
                        if self.state.snakeDirection == "up":
                            toSpeedUp = True
                        elif self.state.snakeDirection != "down":
                            self.state.snakeDirection = "up"
                            self.state.switchingDirection = True

                    elif k == QtCore.Qt.Key_Down:
                        if self.state.snakeDirection == "down":
                            toSpeedUp = True
                        elif self.state.snakeDirection != "up":
                            self.state.snakeDirection = "down"
                            self.state.switchingDirection = True

                    elif k == QtCore.Qt.Key_Left:
                        if self.state.snakeDirection == "left":
                            toSpeedUp = True
                        elif self.state.snakeDirection != "right":
                            self.state.snakeDirection = "left"
                            self.state.switchingDirection = True

                    elif k == QtCore.Qt.Key_Right:
                        if self.state.snakeDirection == "right":
                            toSpeedUp = True
                        elif self.state.snakeDirection != "left":
                            self.state.snakeDirection = "right"
                            self.state.switchingDirection = True

                    if toSpeedUp:
                        self.makeMove()

        # else:
        #     event.accept()

    @staticmethod
    def launch(klass):
        """Receive window class as argument and launch application with this window"""
        app = QApplication(sys.argv)
        window = klass()
        window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    # Launch snake with checkboxes
    SnakeCheckboxes.launch(SnakeCheckboxes)
