"""Helper functions."""
import random
import os
import json
import sys
from copy import deepcopy
from typing import List, Optional
import dataclasses
from dacite import from_dict
from PyQt5.QtWidgets import QCheckBox
import constants as c
import type_declarations as t


def genDefaultMatrix(cellNum: int) -> List[List[t.CellType]]:
    """
    Generate initial game board (with empty cells).

    @param cellNum: width/height of the board (in cells)
    @return: matrix that models game board (with all cells being empty)
    """
    matrix = [
        [t.CellTypes.empty for _ in range(cellNum)] for _ in range(cellNum)
    ]
    return deepcopy(matrix)  # type: ignore


def snakeAndFoodToMatrix(
    snakeSegments: List[t.Coordinate], cellNum: int, food=None
) -> List[List[t.CellType]]:
    """
    Put snake and food into board matrix (2D array).

    @param snakeSegments: array of snake segments (with x and y)
    @param cellNum: width/height of the board (in cells)
    @param food: x and y of food
    @return: matrix that models game board (with snake segments and food)
    """
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
    """
    Check if snake intersects with the food.

    @param snakeSegments: array of snake segments (with x and y)
    @param food: x and y of food
    @return: is snake eating food?
    """
    head = snakeSegments[-1]
    return head.x == food.x and head.y == food.y


def isOut(snakeSegments: List[t.Coordinate], cellNum: int) -> bool:
    """
    Check if snake went out of the board.

    @param snakeSegments: array of snake segments (with x and y)
    @param cellNum: width/height of the board (in cells)
    @return: is snake out of the board?
    """
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
    """
    Check if snake is colliding with itself.

    @param snakeSegments: array of snake segments (with x and y)
    @return: is snake colliding with itself?
    """
    for i, segment in enumerate(snakeSegments):
        for j, segment2 in enumerate(snakeSegments):
            if i != j:
                if segment.x == segment2.x and segment.y == segment2.y:
                    return True
    return False


def generateFoodPosition(snakeSegments: List[t.Coordinate], cellNum: int) -> Optional[t.Coordinate]:
    """
    Generate new random position for food.

    @param snakeSegments: array of snake segments (with x and y)
    @param cellNum: width/height of the board (in cells)
    @return: x and y of new food
    """
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
    """
    Check if settings.json file exists on disk.

    @param fileName: file name to check
    @return: does file exist?
    """
    return os.path.isfile(fileName)


def writeSettingsFile(settings: t.Settings, fileName: str = c.SETTINGS_FILE) -> None:
    """
    Write Settings object into settings.json.

    @param settings: object with settings values
    @param fileName: file name to check
    @return: does file exist?
    """
    with open(fileName, 'w', encoding="utf-8") as f:
        f.write(json.dumps(dataclasses.asdict(settings)))


def readSettingsFile(fileName: str = c.SETTINGS_FILE) -> t.Settings:
    """
    Read settings.json into Settings object.

    @param fileName: file name to check
    @return: object with settings values
    """
    with open(fileName, encoding="utf-8") as f:
        return from_dict(data_class=t.Settings, data=json.load(f))


def validateSettings(settings: t.Settings) -> bool:
    """
    Validate user input. All fields should be present. Values should not be below zero.

    @param settings: object with settings values
    @return: is user input valid?
    """
    keys = [field.name for field in dataclasses.fields(t.Settings)]

    for key in ["checkIsOut", "checkIsColliding", "disableTimer"]:
        if key not in keys or not isinstance(getattr(settings, key), bool):
            return False

    for key in ["cellNum", "intervalMilliseconds", "cellSize"]:
        if (
            key not in keys or
            not isinstance(getattr(settings, key), int) or
            getattr(settings, key) < 0
        ):
            return False

    if settings.cellNum < 2:
        return False
    
    if settings.cellSize < 1:
        return False
    
    return True


def readOrCreateSettings(defaultSettings: t.Settings = c.DEFAULT_SETTINGS) -> t.Settings:
    """
    Read settings.json. If it doesn't exist, create it and fill it with default values.

    @param defaultSettings: object with default settings
    @return: settings that were read from file
    """
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


def genStyleSheet(color1: str, color2: str = "#fff") -> str:
    """
    Generate checkbox css (it should be diffirent in windows and linux).

    @param color1: first color of checkbox
    @param color2: second color of checkbox (can be used only in linux)
    @return: css for QCheckBox
    """
    if sys.platform == "win32":
        return ("QCheckBox::indicator {" +
                "background-color: " + color1 + "; "
                "}"
                )

    return "color: " + color2 + ";" + "background-color: " + color1


def matrixToCheckboxes(matrix: List[List[t.CellType]], checkboxes: List[QCheckBox]):
    """
    Render 2D array to checkboxes.

    @param matrix: 2D array that describes game board
    @param checkboxes: array of QCheckBox that would be marked/unmarked
    """
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == t.CellTypes.empty:
                checkboxes[y][x].setChecked(False)
                checkboxes[y][x].setStyleSheet(genStyleSheet(c.CHECKBOX_COLORS.empty))
            else:
                checkboxes[y][x].setChecked(True)
                if value == t.CellTypes.snakeSegment:
                    color = c.CHECKBOX_COLORS.snakeSegment
                elif value == t.CellTypes.snakeHead:
                    color = c.CHECKBOX_COLORS.snakeHead
                elif value == t.CellTypes.food:
                    color = c.CHECKBOX_COLORS.food

                checkboxes[y][x].setStyleSheet(
                    genStyleSheet(color))
