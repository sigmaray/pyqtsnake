import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QtWidgets.QLabel()
        self.label.setFixedSize(400, 300)
        canvas = QtGui.QPixmap(400, 300)
        self.label.setPixmap(canvas)
        # self.setCentralWidget(self.label)
        self.layout.addWidget(self.label)

        # self.draw_something()
        self.painter = QtGui.QPainter(self.label.pixmap())
        self.drawRectangle(self.painter, 0, 0, 20, 20)

        self.drawRectangle(self.painter, 20, 20, 20, 20)

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
        pen = QtGui.QPen()
        pen.setWidth(15)
        pen.setColor(QtGui.QColor('blue'))
        painter.setPen(pen)
        painter.drawLine(
            QtCore.QPoint(100, 100),
            QtCore.QPoint(300, 200)
        )
        # painter.end()

    def drawRectangle(self,
                      painter,
                      x,
                      y,
                      w,
                      h,
                      color="#ccc",
                      borderColor="SlateBlue",
                      border=None,
                      margin=None):
        if (border == None):
            border = w * 0.05
        if (margin == None):
            margin = w * 0.1

        pen = QtGui.QPen()
        # pen.setWidth(15)
        pen.setColor(QtGui.QColor(borderColor))
        painter.setPen(pen)
        # painter.drawLine(
        #     QtCore.QPoint(100, 100),
        #     QtCore.QPoint(300, 200)
        # )
        painter.setBrush(QBrush(QtGui.QColor(color), Qt.SolidPattern))
        painter.drawRect(x, y, w, h)

        # painter.end()

    # const drawRectangle = (
    #     ctx,
    #     x,
    #     y,
    #     w,
    #     h,
    #     color="#ccc",
    #     borderColor="SlateBlue",
    #     border=null,
    #     margin=null
    # ) = > {
    #     if (border == = null) border = w * 0.05
    #     if (margin == = null) margin = w * 0.1

    #     ctx.fillStyle = borderColor
    #     ctx.fillRect(x + margin, y + margin, w - margin * 2, h - margin * 2)
    #     ctx.fillStyle = color
    #     ctx.fillRect(
    #         x + border + margin,
    #         y + border + margin,
    #         w - border * 2 - margin * 2,
    #         h - border * 2 - margin * 2
    #     )
    # }


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
