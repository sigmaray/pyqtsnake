"""Helper functions for graphical Snake."""
from typing import List
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
from PyQt5.QtCore import Qt
import type_declarations as t
import constants


def matrixToCanvas(matrix: List[List[t.CellType]], cellSize: int, painter: QPainter):
    """
    Paint 2D array on canvas.

    @param matrix: 2D array that describes game board
    @param cellSize: width/height of the board (in cells)
    @param painter: canvas painter that will be used to draw the cells
    """
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == t.CellTypes.empty:
                drawEmpty(painter, x * cellSize, y *
                          cellSize, cellSize)
            else:
                if value == t.CellTypes.snakeSegment:
                    drawSnakeSegment(painter, x * cellSize,
                                     y * cellSize, cellSize)
                elif value == t.CellTypes.snakeHead:
                    drawSnakeHead(painter, x * cellSize, y *
                                  cellSize, cellSize)
                elif value == t.CellTypes.food:
                    drawFood(painter, x * cellSize, y *
                             cellSize, cellSize)


def drawRectangle(
    painter: QPainter,
    x: int,
    y: int,
    size: int,
    backgroundColor: str = "#ccc",
    borderColor: str = constants.CANVAS_COLORS.border,
    border=None,
    margin=None
):
    """
    Draw board cell on canvas.

    @param painter: canvas painter that will be used to draw the cells
    @param x: x of left upper corner of board cell to be drawn
    @param y: y of left upper corner of board cell to be drawn
    @param width: cell width/height
    @param backgroundColor: cell background color
    @param borderColor: cell border color

    """
    b = border
    m = margin

    if b is None:
        b = int(size * 0.05)
    if m is None:
        m = int(size * 0.1)

    pen = QPen()
    pen.setColor(QColor(borderColor))
    painter.setPen(pen)
    painter.setBrush(QBrush(QColor(backgroundColor), Qt.SolidPattern))  # type: ignore
    painter.drawRect(x + b + m, y + b + m, size - b * 2 - m * 2, size - b * 2 - m * 2)


def drawEmpty(
        painter: QPainter,
        x: int,
        y: int,
        size: int,
        backgroundColor: str = constants.CANVAS_COLORS.emptyBackground,
        borderColor: str = constants.CANVAS_COLORS.border
):
    """
    Draw empty cell on canval (without snake or food).

    @param painter: canvas painter that will be used to draw empty cell
    @param x: x of left upper corner of empty cell to be drawn
    @param y: y of left upper corner of empty cell to be drawn
    @param width: empty cell width/height
    @param backgroundColor: empty cell background color
    @param borderColor: empty cell border color
    """
    drawRectangle(
        painter,
        x,
        y,
        size,
        backgroundColor,
        borderColor
    )


def drawSnakeSegment(
        painter: QPainter,
        x: int,
        y: int,
        size: int,
        backgroundColor: str = constants.CANVAS_COLORS.snakeSegmentBackground,
        borderColor: str = constants.CANVAS_COLORS.border
):
    """
    Draw snake body.

    @param painter: canvas painter that will be used to draw snake segment
    @param x: x of left upper corner of snake segment to be drawn
    @param y: y of left upper corner of snake segment to be drawn
    @param width: snake segment width/height
    @param backgroundColor: snake segment background color
    @param borderColor: snake segment border color
    """
    drawRectangle(
        painter,
        x,
        y,
        size,
        backgroundColor,
        borderColor,
    )


def drawSnakeHead(
        painter: QPainter,
        x: int,
        y: int,
        size: int,
        backgroundColor: str = constants.CANVAS_COLORS.snakeHeadBackground,
        borderColor: str = constants.CANVAS_COLORS.border
):
    """
    Draw snake head (head can have different color).

    @param painter: canvas painter that will be used to draw snake head
    @param x: x of left upper corner of snake head to be drawn
    @param y: y of left upper corner of snake head to be drawn
    @param width: snake head width/height
    @param backgroundColor: snake head background color
    @param borderColor: snake head border color
    """
    drawRectangle(
        painter,
        x,
        y,
        size,
        backgroundColor,
        borderColor
    )


def drawFood(
        painter: QPainter,
        x: int,
        y: int,
        size: int,
        backgroundColor: str = constants.CANVAS_COLORS.foodBackground,
        borderColor: str = constants.CANVAS_COLORS.border):
    """
    Draw food.

    @param painter: canvas painter that will be used to draw food
    @param x: x of left upper corner of food to be drawn
    @param y: y of left upper corner of food to be drawn
    @param width: food width/height
    @param backgroundColor: food background color
    @param borderColor: food border color
    """
    drawRectangle(
        painter,
        x,
        y,
        size,
        backgroundColor,
        borderColor
    )
