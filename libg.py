"""Helper functions for graphical Snake"""
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt
from constants import CELL_TYPES


def matrixToCanvas(matrix, CELL_SIZE, painter):
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == CELL_TYPES.empty:
                drawEmpty(painter, x * CELL_SIZE, y *
                          CELL_SIZE, CELL_SIZE, CELL_SIZE)
            else:
                if value == CELL_TYPES.snakeSegment:
                    drawSnakeSegment(painter, x * CELL_SIZE,
                                     y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                elif value == CELL_TYPES.snakeHead:
                    drawSnakeHead(painter, x * CELL_SIZE, y *
                                  CELL_SIZE, CELL_SIZE, CELL_SIZE)
                elif value == CELL_TYPES.food:
                    drawFood(painter, x * CELL_SIZE, y *
                             CELL_SIZE, CELL_SIZE, CELL_SIZE)


def drawRectangle(
        painter,
        x,
        y,
        w,
        h,
        color="#ccc",
        borderColor="SlateBlue",
        border=None,
        margin=None):
    if border is None:
        border = w * 0.05
    if margin is None:
        margin = w * 0.1

    pen = QPen()
    # pen.setWidth(1)
    pen.setColor(QColor(borderColor))
    painter.setPen(pen)
    # painter.drawLine(
    #     QtCore.QPoint(100, 100),
    #     QtCore.QPoint(300, 200)
    # )
    painter.setBrush(QBrush(QColor(color), Qt.SolidPattern))

    painter.drawRect(x, y, w - 1, h - 1)


def drawEmpty(
        painter,
        x,
        y,
        w,
        h,
        color="#ccc",
        borderColor="SlateBlue",
        border=None,
        margin=None):
    drawRectangle(
        painter,
        x,
        y,
        w,
        h,
        color,
        borderColor,
        border,
        margin)


def drawSnakeSegment(
        painter,
        x,
        y,
        w,
        h,
        color="blue",
        borderColor="SlateBlue",
        border=None,
        margin=None):
    drawRectangle(
        painter,
        x,
        y,
        w,
        h,
        color,
        borderColor,
        border,
        margin)


def drawSnakeHead(
        painter,
        x,
        y,
        w,
        h,
        color="blue",
        borderColor="SlateBlue",
        border=None,
        margin=None):
    drawRectangle(
        painter,
        x,
        y,
        w,
        h,
        color,
        borderColor,
        border,
        margin)


def drawFood(
        painter,
        x,
        y,
        w,
        h,
        color="red",
        borderColor="SlateBlue",
        border=None,
        margin=None):
    drawRectangle(
        painter,
        x,
        y,
        w,
        h,
        color,
        borderColor,
        border,
        margin)
