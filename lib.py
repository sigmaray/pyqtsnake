from constants import *
import random


def gen_default_matrix(cellNum):
    return [
        [CELL_TYPES.empty] * cellNum
    ] * cellNum


def snakeAndFoodToMatrix(snakeSegments, cellNum, food=None):
    matrix = gen_default_matrix(cellNum)

    for i, segment in enumerate(snakeSegments):
        if i == len(snakeSegments) - 1:
            type = CELL_TYPES.snakeHead
        else:
            type = CELL_TYPES.snakeSegment

        matrix[segment["x"]][segment["y"]] = type

    if food:
        matrix[food["y"]][food["x"]] = CELL_TYPES.food

    return matrix


def generateFoodPosition(snakeSegments, cellNum, food=None):
    matrix = snakeAndFoodToMatrix(snakeSegments, cellNum)
    availableCells = []
#   matrix.forEach((row, y)= > {
    for y, row in enumerate(matrix):
        # row.forEach((value, x)= > {
        for x, value in enumerate(row):
            if value == CELL_TYPES.empty:
                availableCells.append({
                    "x": x,
                    "y": y
                })

    return random.choice(availableCells)
