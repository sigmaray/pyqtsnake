from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from constants import *
from libg import *

from snake import SnakeCheckboxes

class SnakeCanvas(SnakeCheckboxes):
    CELL_SIZE = 20

    def addBoard(self):
        boardSize = self.CELL_SIZE * self.settings.cellNum

        self.label = QLabel()
        # self.label.setFixedSize(boardSize, boardSize)
        self.layout.addWidget(self.label)
        canvas = QtGui.QPixmap(boardSize, boardSize)
        self.label.setPixmap(canvas)
        self.painter = QtGui.QPainter(self.label.pixmap())

    def render(self, matrix):
        matrixToCanvas(matrix, self.CELL_SIZE, self.painter)
        self.update()

if __name__ == "__main__":
    SnakeCanvas.launch(SnakeCanvas)
