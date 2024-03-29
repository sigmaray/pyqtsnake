#!/usr/bin/python3
"""Snake game with checkboxes."""
from copy import deepcopy
import sys
import os
from typing import Literal, List
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QToolBar, QAction,
                             QLabel, QHBoxLayout, QCheckBox, QMessageBox)
from munch import Munch
from settings_dialog import SettingsDialog
import lib
import type_declarations as t
import constants as c


class SnakeCheckboxes(QWidget):
    """PyQt window."""

    # Add some content to prevent form elements moving
    LABEL_PLACEHOLDER = " "

    state: t.State

    # Put all widgets inside the scope
    widgets = Munch()

    def __init__(self):
        """
        Initialize the game.

        * Read (or create) settings.
        * Create UI elements.
        * Generate default state.
        * Create and start timer.
        """
        super().__init__()

        self.settings = lib.readOrCreateSettings()

        self.state = self.generateState()

        self.widgets.layout = QVBoxLayout()
        self.setLayout(self.widgets.layout)

        self.addToolbar()

        self.addBoard()

        self.widgets.labelStatus = QLabel(self.LABEL_PLACEHOLDER)
        self.widgets.layout.addWidget(self.widgets.labelStatus)

        matrix = lib.snakeAndFoodToMatrix(self.state.snakeSegments,
                                          self.settings.cellNum, self.state.food)
        self.renderGame(matrix)

        if not self.settings.disableTimer:
            self.addTimer()

    def addTimer(self):
        """Add timer and connect it to handler function."""
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(self.settings.intervalMilliseconds)

    def generateState(self):
        """Generate initial game state."""
        snakeSegments = [
            t.Coordinate(x=0, y=0)
        ]

        return t.State(
            snakeDirection="right",
            isPaused=False,
            snakeSegments=snakeSegments,
            food=lib.generateFoodPosition(
                snakeSegments, self.settings.cellNum),
            switchingDirection=False
        )

    def onClickRestart(self):
        """When Restart button is clicked: restart the game."""
        self.state = self.generateState()
        self.widgets.labelStatus.setText(self.LABEL_PLACEHOLDER)
        matrix = lib.snakeAndFoodToMatrix(self.state.snakeSegments,
                                          self.settings.cellNum, self.state.food)
        self.renderGame(matrix)
        if not self.settings.disableTimer:
            self.timer.start(self.settings.intervalMilliseconds)

    def pause(self):
        """Pause the game."""
        self.state.isPaused = True
        self.timer.stop()
        self.widgets.labelStatus.setText("paused")

    def unpause(self):
        """Unpause the game."""
        self.state.isPaused = False
        self.timer.start(self.settings.intervalMilliseconds)
        self.widgets.labelStatus.setText(self.LABEL_PLACEHOLDER)

    def onTogglePauseClick(self):
        """When user clicked on Pause or Unpause button."""
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
        End the game.

        * Show a message to user
        * Stop timer

        @param message: message that will be shown to user
        """
        self.widgets.labelStatus.setText(message)
        if not self.settings.disableTimer:
            self.timer.stop()

    def onTimer(self):
        """When timer is triggerd: do the next iteration of the game."""
        self.makeMove()

    def makeMove(self):
        """
        When timer is called or when user presses same button a few times.

        * Move snake by one cell
        * Check if food is eaten (generate new random food and increase snake lenght)
        * Check if game is over
        * Call renderer
        """
        # If there is no food game is over and we can't continue
        if not self.state.food:
            return

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

        self.state.snakeSegments.append(newHead)

        ateFood = lib.isEating(self.state.snakeSegments, self.state.food)

        if not ateFood:
            self.state.snakeSegments.pop(0)
        else:
            self.state.food = lib.generateFoodPosition(
                self.state.snakeSegments, self.settings.cellNum)
            if not self.state.food:
                self.endGame("You won!\nPress F5 or click \"Restart\" button")
                return

        if self.settings.checkIsOut and lib.isOut(self.state.snakeSegments, self.settings.cellNum):
            self.endGame("Snake is out of board. You lost")
            return

        if self.settings.checkIsColliding and lib.isColliding(self.state.snakeSegments):
            self.endGame("Snake collision. You lost")
            return

        matrix = lib.snakeAndFoodToMatrix(self.state.snakeSegments,
                                          self.settings.cellNum, self.state.food)

        self.renderGame(matrix)

        self.state.switchingDirection = False

    def determineDelta(self, currentInterval: int, direction: Literal["up", "down"]):
        """
        Determine how fast to change the interval (when user clicks button).

        If interval is small and change it slower.
        If it is large change it faster.

        @param currentInterval: old interval
        @param direction: should increase or decrease?
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
        """Speed up snake (when user clicks UI button or presses PageDown)."""
        self.settings.intervalMilliseconds -= self.determineDelta(
            self.settings.intervalMilliseconds, "down")

        lib.writeSettingsFile(self.settings)

        self.widgets.speedLabel.setText(
            str(self.settings.intervalMilliseconds))

        self.timer.stop()
        self.timer.start(self.settings.intervalMilliseconds)

    def onIntervalIncrClick(self):
        """Slow down snake (when user clicks UI button or presses PageUp."""
        self.settings.intervalMilliseconds += self.determineDelta(
            self.settings.intervalMilliseconds, "up")

        lib.writeSettingsFile(self.settings)

        self.widgets.speedLabel.setText(
            str(self.settings.intervalMilliseconds))

        self.timer.stop()
        self.timer.start(self.settings.intervalMilliseconds)

    def onShowSettingsClick(self):
        """When user clicks Settings button."""
        if not self.settings.disableTimer:
            self.pause()
        settings, result = SettingsDialog.run(self.settings)
        if result:
            lib.writeSettingsFile(settings)

            # https://stackoverflow.com/a/62611055
            QtCore.QCoreApplication.quit()
            QtCore.QProcess.startDetached(sys.executable, sys.argv)
        else:
            if not self.settings.disableTimer:
                self.unpause()

    def onResetSettingsClick(self):
        """When user clicks Settings button."""
        if not self.settings.disableTimer:
            self.pause()

        quit_msg = "Are you sure you want to reset settings to default values and restart the game?"
        reply = QMessageBox.question(self, 'Message',
                                     quit_msg, QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            os.remove(c.SETTINGS_FILE)

            # https://stackoverflow.com/a/62611055
            QtCore.QCoreApplication.quit()
            QtCore.QProcess.startDetached(sys.executable, sys.argv)
        else:
            if not self.settings.disableTimer:
                self.unpause()

    def onShowHelpClick(self):
        """When user clicks Help button: show help message."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Help")
        msg.setText("""
Controls:
* Pause/unpause: P key
* Move snake: Left/Right/Up/Down keys
* Restart: F5
* Decrease speed: PgUp
* Increase speed: PgDown
        """)
        msg.exec_()

    def addToolbar(self):
        """Add toolbars with control buttons, bind buttons to click handlers."""
        self.widgets.toolBar = QToolBar()
        self.widgets.layout.addWidget(self.widgets.toolBar)

        actionPauseUnpause = QAction("Interval-", self)
        actionPauseUnpause.triggered.connect(self.onIntervalDecrClick)
        self.widgets.toolBar.addAction(actionPauseUnpause)

        self.widgets.speedLabel = QLabel(
            str(self.settings.intervalMilliseconds))
        self.widgets.toolBar.addWidget(self.widgets.speedLabel)

        actionIntervalPlus = QAction("Interval+", self)
        actionIntervalPlus.triggered.connect(self.onIntervalIncrClick)
        self.widgets.toolBar.addAction(actionIntervalPlus)

        self.widgets.toolBar2 = QToolBar()
        self.widgets.layout.addWidget(self.widgets.toolBar2)

        actionPauseUnpause = QAction("(Un)pause", self)
        actionPauseUnpause.triggered.connect(self.onTogglePauseClick)
        self.widgets.toolBar2.addAction(actionPauseUnpause)

        actionRestart = QAction("Restart", self)
        actionRestart.triggered.connect(self.onClickRestart)
        self.widgets.toolBar2.addAction(actionRestart)

        actionSettings = QAction("Settings", self)
        actionSettings.triggered.connect(self.onShowSettingsClick)
        self.widgets.toolBar2.addAction(actionSettings)

        self.widgets.toolBar3 = QToolBar()
        self.widgets.layout.addWidget(self.widgets.toolBar3)

        actionReset = QAction("Reset settings", self)
        actionReset.triggered.connect(self.onResetSettingsClick)
        self.widgets.toolBar3.addAction(actionReset)

        actionHelp = QAction("Help", self)
        actionHelp.triggered.connect(self.onShowHelpClick)
        self.widgets.toolBar3.addAction(actionHelp)

        self.widgets.toolBar4 = QToolBar()
        self.widgets.layout.addWidget(self.widgets.toolBar4)

    def renderGame(self, matrix: List[List[t.CellType]]):
        """
        Render 2D array to checkboxes.

        @param matrix: 2D array that describes game board
        """
        lib.matrixToCheckboxes(matrix, self.widgets.checkboxes)

    def addBoard(self):
        """Add board that will contain snake and food: create layout and checkboxes."""
        self.widgets.checkboxes = []
        for _ in range(self.settings.cellNum):
            row = []

            hl = QHBoxLayout()

            for _ in range(self.settings.cellNum):
                checkbox = QCheckBox()
                checkbox.setEnabled(False)
                hl.addWidget(checkbox)
                row.append(checkbox)

            self.widgets.checkboxes.append(row)
            self.widgets.layout.addLayout(hl)

    def keyPressEvent(self, event):
        """
        When user presses keyboard button.

        * Change direction (if user pressesed different button).
        * Move snake faster (when user presses same button one more time).
        * Pause/unpase (when user clicked P button).
        * Increase speed (when user presses PageDown).
        * Decrease speed (when user presses PageUp).
        """
        allowedKeys = [
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_P,
            1047,  # "p" in russian layout
            QtCore.Qt.Key_F5,
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
            elif event.key() == QtCore.Qt.Key_F5:
                self.onClickRestart()
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

                    if toSpeedUp or self.settings.disableTimer:
                        self.makeMove()

        # else:
        #     event.accept()

    @staticmethod
    def launch(klass):
        """Receive window class as argument and launch application with this window."""
        app = QApplication(sys.argv)
        window = klass()
        window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    # Launch snake with checkboxes
    SnakeCheckboxes.launch(SnakeCheckboxes)
