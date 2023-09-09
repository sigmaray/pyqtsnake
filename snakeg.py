#!/usr/bin/python3
"""Snake game with canvas."""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel
import libg
from snake import SnakeCheckboxes


class SnakeCanvas(SnakeCheckboxes):
    """PyQt window (with canvas instead of checkboxes)."""

    # Width and height of a single game cell
    CELL_SIZE = 20

    def addBoard(self):
        """Override method of parent class: create canvas instead of checkboxes."""
        boardSize = self.CELL_SIZE * self.settings.cellNum

        self.widgets.label = QLabel()
        # self.label.setFixedSize(boardSize, boardSize)
        self.widgets.layout.addWidget(self.widgets.label)
        canvas = QtGui.QPixmap(boardSize, boardSize)
        self.widgets.label.setPixmap(canvas)
        self.widgets.painter = QtGui.QPainter(self.widgets.label.pixmap())

    def renderGame(self, matrix):
        """Override method of parent class: render to canvas instead of checkboxes."""
        libg.matrixToCanvas(matrix, self.CELL_SIZE, self.widgets.painter)
        self.update()


if __name__ == "__main__":
    # Launch snake with canvas instead of checkboxes
    SnakeCanvas.launch(SnakeCanvas)
