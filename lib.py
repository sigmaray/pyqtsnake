"""Helper functions"""
import random
import os
import json
import sys
from copy import deepcopy
from typing import List
import dataclasses
from dacite import from_dict
from PyQt5.QtWidgets import QCheckBox
import constants as c
import type_declarations as t


def genDefaultMatrix(cellNum: int) -> List[List[t.CellType]]:
    """Generate default game board (with empty cells)"""
    matrix = [
        [t.CellTypes.empty for _ in range(cellNum)] for _ in range(cellNum)
    ]
    return deepcopy(matrix)  # type: ignore


def snakeAndFoodToMatrix(
    snakeSegments: List[t.Coordinate], cellNum: int, food=None
) -> List[List[t.CellType]]:
    """Put snake and food into board matrix (2D array)"""
    matrix = genDefaultMatrix(cellNum)

    for i, segment in enumerate(snakeSegments):
        if i == len(snakeSegments) - 1:
            cellType = t.CellTypes.snakeHead
        else:
            cellType = t.CellTypes.snakeSegment

        matrix[segment.y][segment.x] = cellType

    if food:
        matrix[food.y][food.x] = t.CellTypes.food

    return matrix


def isEating(snakeSegments: List[t.Coordinate], food) -> bool:
    """Check if snake intersects with the food"""
    head = snakeSegments[-1]
    return head.x == food.x and head.y == food.y


def isOut(snakeSegments: List[t.Coordinate], cellNum: int) -> bool:
    """Check if snake went out of the board"""
    for segment in snakeSegments:
        if (
            segment.x < 0 or
            segment.x > cellNum - 1 or
            segment.y < 0 or
            segment.y > cellNum - 1
        ):
            return True
    return False


def isColliding(snakeSegments: List[t.Coordinate]) -> bool:
    """Check if snake is colliding with itself"""
    for i, segment in enumerate(snakeSegments):
        for j, segment2 in enumerate(snakeSegments):
            if i != j:
                if segment.x == segment2.x and segment.y == segment2.y:
                    return True
    return False


def generateFoodPosition(snakeSegments: List[t.Coordinate], cellNum: int):
    """Generate new random position for food not intersecting with snake"""
    matrix = snakeAndFoodToMatrix(snakeSegments, cellNum)
    availableCells = []
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == t.CellTypes.empty:
                availableCells.append(t.Coordinate(
                    x=x,
                    y=y
                ))

    if len(availableCells) == 0:
        return None
    return random.choice(availableCells)


def doSettingsExist(fileName: str = c.SETTINGS_FILE) -> bool:
    """Check if settings.json file exists"""
    return os.path.isfile(fileName)


def writeSettingsFile(settings: t.Settings, fileName: str = c.SETTINGS_FILE) -> None:
    """Write Settings object into settings.json"""
    with open(fileName, 'w', encoding="utf-8") as f:
        f.write(json.dumps(dataclasses.asdict(settings)))


def readSettingsFile(fileName: str = c.SETTINGS_FILE) -> t.Settings:
    """Read settings.json Settings object"""
    with open(fileName, encoding="utf-8") as f:
        return from_dict(data_class=t.Settings, data=json.load(f))


def validateSettings(settings: t.Settings) -> bool:
    """Validate user input. All fields should be present. Values should not be below zero."""
    keys = [field.name for field in dataclasses.fields(t.Settings)]

    for key in ["checkIsOut", "checkIsColliding"]:
        if key not in keys or not isinstance(getattr(settings, key), bool):
            return False

    for key in ["cellNum", "intervalMilliseconds"]:
        if (
            key not in keys or
            not isinstance(getattr(settings, key), int) or
            getattr(settings, key) < 0
        ):
            return False

    if settings.cellNum < 2:
        return False

    return True


def readOrCreateSettings(defaultSettings: t.Settings = c.DEFAULT_SETTINGS) -> t.Settings:
    """Read settings.json. If it doesn't exist, create it and fill it with default values"""
    if not doSettingsExist():
        print("settings.json does not exist, creating it")
        writeSettingsFile(defaultSettings)

    settings = readSettingsFile()

    if not validateSettings(settings):
        print("settings.json is not valid. " +
              "You can delete it and restart the application. " +
              "App will recreate settings file if it's not present")
        sys.exit()

    return settings


def genStyleSheet(backgroundColor: str = "#fff", color: str = "#fff") -> str:
    """Generate checkbox css (it should be diffirent in windows and linux)"""
    if sys.platform == "win32":
        return ("QCheckBox::indicator {" +
                "background-color: " + color + "; "
                "}"
                )

    return "color: " + color + ";" + "background-color: " + backgroundColor


def matrixToCheckboxes(matrix: List[List[t.CellType]], checkboxes: List[QCheckBox]):
    """Render 2D array to checkboxes"""
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == t.CellTypes.empty:
                checkboxes[y][x].setChecked(False)
                checkboxes[y][x].setStyleSheet(genStyleSheet('#fff'))
            else:
                checkboxes[y][x].setChecked(True)
                if value == t.CellTypes.snakeSegment:
                    color = c.CHECKBOX_COLORS.snakeSegment
                    backgroundColor = "#fff"
                elif value == t.CellTypes.snakeHead:
                    color = c.CHECKBOX_COLORS.snakeHead
                    backgroundColor = "#ccc"
                elif value == t.CellTypes.food:
                    color = c.CHECKBOX_COLORS.food
                    backgroundColor = "#ccc"

                checkboxes[y][x].setStyleSheet(
                    genStyleSheet(backgroundColor, color))
