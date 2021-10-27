import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QtWidgets.QLabel()
        self.label.setFixedSize(400, 300)
        self.layout.addWidget(self.label)
        canvas = QtGui.QPixmap(400, 300)
        self.label.setPixmap(canvas)
        # self.setCentralWidget(self.label)
        self.draw_something()

    # def draw_something(self):
    #     painter = QtGui.QPainter(self.label.pixmap())
    #     painter.drawLine(10, 10, 300, 200)
    #     painter.end()

    # def draw_something(self):
    #     painter = QtGui.QPainter(self.label.pixmap())
    #     pen = QtGui.QPen()
    #     pen.setWidth(40)
    #     pen.setColor(QtGui.QColor('red'))
    #     painter.setPen(pen)
    #     painter.drawPoint(200, 150)
    #     painter.end()

    def draw_something(self):
        from random import randint
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(15)
        pen.setColor(QtGui.QColor('blue'))
        painter.setPen(pen)
        painter.drawLine(
            QtCore.QPoint(100, 100),
            QtCore.QPoint(300, 200)
        )
        painter.end()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
