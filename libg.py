"""Helper functions for graphical Snake"""
from typing import List
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
from PyQt5.QtCore import Qt
import type_declarations as t
import constants


def matrixToCanvas(matrix: List[List[t.CellType]], cellSize: int, painter: QPainter):
    """Paint 2D array on canvas"""
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == t.CellTypes.empty:
                drawEmpty(painter, x * cellSize, y *
                          cellSize, cellSize, cellSize)
            else:
                if value == t.CellTypes.snakeSegment:
                    drawSnakeSegment(painter, x * cellSize,
                                     y * cellSize, cellSize, cellSize)
                elif value == t.CellTypes.snakeHead:
                    drawSnakeHead(painter, x * cellSize, y *
                                  cellSize, cellSize, cellSize)
                elif value == t.CellTypes.food:
                    drawFood(painter, x * cellSize, y *
                             cellSize, cellSize, cellSize)


def drawRectangle(
        painter: QPainter,
        x: int,
        y: int,
        width: int,
        height: int,
        color: str = "#ccc",
        borderColor: str = constants.CANVAS_COLORS.border):
    """Draw board cell on canvas"""
    pen = QPen()
    # pen.setWidth(1)
    pen.setColor(QColor(borderColor))
    painter.setPen(pen)
    painter.setBrush(QBrush(QColor(color), Qt.SolidPattern))  # type: ignore
    painter.drawRect(x, y, width - 1, height - 1)


def drawEmpty(
        painter: QPainter,
        x: int,
        y: int,
        width: int,
        height: int,
        backgroundColor: str = constants.CANVAS_COLORS.emptyBackground,
        borderColor: str = constants.CANVAS_COLORS.border
):
    """Draw empty cell on canval (without snake or food)"""
    drawRectangle(
        painter,
        x,
        y,
        width,
        height,
        backgroundColor,
        borderColor
    )


def drawSnakeSegment(
        painter: QPainter,
        x: int,
        y: int,
        widht: int,
        height: int,
        backgroundColor: str = constants.CANVAS_COLORS.snakeSegmentBackground,
        borderColor: str = constants.CANVAS_COLORS.border
):
    """Draw snake body"""
    drawRectangle(
        painter,
        x,
        y,
        widht,
        height,
        backgroundColor,
        borderColor,
    )


def drawSnakeHead(
        painter: QPainter,
        x: int,
        y: int,
        width: int,
        height: int,
        backgroundColor: str = constants.CANVAS_COLORS.snakeHeadBackground,
        borderColor: str = constants.CANVAS_COLORS.border
):
    """Draw snake head (head can have different color)"""
    drawRectangle(
        painter,
        x,
        y,
        width,
        height,
        backgroundColor,
        borderColor
    )


def drawFood(
        painter: QPainter,
        x: int,
        y: int,
        width: int,
        height: int,
        backgroundColor: str = constants.CANVAS_COLORS.foodBackground,
        borderColor: str = constants.CANVAS_COLORS.border):
    """Draw food"""
    drawRectangle(
        painter,
        x,
        y,
        width,
        height,
        backgroundColor,
        borderColor
    )
