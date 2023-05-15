"""Helper functions"""
import random
import os
import json
import sys
from munch import munchify
import constants


def deep_copy(o):
    return json.loads(json.dumps(o))


def gen_default_matrix(cellNum):
    matrix = [
        [constants.CELL_TYPES.empty] * cellNum
    ] * cellNum
    return deep_copy(matrix)


def snakeAndFoodToMatrix(snakeSegments, cellNum, food=None):
    matrix = gen_default_matrix(cellNum)

    for i, segment in enumerate(snakeSegments):
        if i == len(snakeSegments) - 1:
            cellType = constants.CELL_TYPES.snakeHead
        else:
            cellType = constants.CELL_TYPES.snakeSegment

        matrix[segment["y"]][segment["x"]] = cellType

    if food:
        matrix[food["y"]][food["x"]] = constants.CELL_TYPES.food

    return matrix


def isEating(snakeSegments, food):
    head = snakeSegments[-1]
    return head.x == food.x and head.y == food.y


def isOut(snakeSegments, cellNum):
    for segment in snakeSegments:
        if (
            segment.x < 0 or
            segment.x > cellNum - 1 or
            segment.y < 0 or
            segment.y > cellNum - 1
        ):
            return True
    return False


def isColliding(snakeSegments):
    for i, segment in enumerate(snakeSegments):
        for j, segment2 in enumerate(snakeSegments):
            if i != j:
                if segment.x == segment2.x and segment.y == segment2.y:
                    return True
    return False


def generateFoodPosition(snakeSegments, cellNum):
    matrix = snakeAndFoodToMatrix(snakeSegments, cellNum)
    availableCells = []
#   matrix.forEach((row, y)= > {
    for y, row in enumerate(matrix):
        # row.forEach((value, x)= > {
        for x, value in enumerate(row):
            if value == constants.CELL_TYPES.empty:
                availableCells.append({
                    "x": x,
                    "y": y
                })

    if len(availableCells) == 0:
        return None
    return munchify(random.choice(availableCells))

# def createSettings:


def doSettingsExist():
    return os.path.isfile(constants.SETTINGS_FILE)


def writeSettingsFile(hashmap):
    with open(constants.SETTINGS_FILE, 'w', encoding="utf-8") as f:
        f.write(json.dumps(hashmap))


def readSettingsFile():
    with open(constants.SETTINGS_FILE, encoding="utf-8") as f:
        return json.load(f)


def validateSettings(settings):

    for key in ["checkIsOut", "checkIsColliding"]:
        if not(key in settings.keys()) or not isinstance(settings[key], bool):
            return False

    for key in ["cellNum", "intervalMilliseconds"]:
        if not(key in settings.keys()) or not isinstance(settings[key], int) or (settings[key] < 0):
            return False

    if settings["cellNum"] < 2:
        return False

    return True


# settings = {
#     "canvasSize": 500,
#     "cellNum": 15,
#     "intervalMilliseconds": 150,
#     "checkIsOut": False,
#     "checkIsColliding": False,
# }

def readWriteSettings():
    if not doSettingsExist():
        print("settings.json does not exist, creating it")
        writeSettingsFile(constants.DEFAULT_SETTINGS)

    settings = readSettingsFile()

    if not validateSettings(settings):
        print("settings.json is not valid. " +
              "You can delete it and restart the application. " +
              "App will recreate settings file if it's not present")
        sys.exit()

    return settings


def genStyleSheet(backgroundColor="#fff", color="#fff"):
    if sys.platform == "win32":
        return ("QCheckBox::indicator {" +
                "background-color: " + color + "; "
                "}"
                )

    return "color: " + color + ";" + "background-color: " + backgroundColor


def matrixToCheckboxes(matrix, checkboxes):
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == constants.CELL_TYPES.empty:
                checkboxes[y][x].setChecked(False)
                checkboxes[y][x].setStyleSheet(genStyleSheet('#fff'))
            else:
                checkboxes[y][x].setChecked(True)
                if value == constants.CELL_TYPES.snakeSegment:
                    color = constants.COLORS.snakeSegment
                    backgroundColor = "#fff"
                elif value == constants.CELL_TYPES.snakeHead:
                    color = constants.COLORS.snakeHead
                    backgroundColor = "#ccc"
                elif value == constants.CELL_TYPES.food:
                    color = constants.COLORS.food
                    backgroundColor = "#ccc"

                checkboxes[y][x].setStyleSheet(
                    genStyleSheet(backgroundColor, color))
