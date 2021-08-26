from constants import *
import random
import os
import json
import sys


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

# def createSettings:


def doSettingsExist():
    return os.path.isfile(SETTINGS_FILE)


def createSettingsFile():
    # file = open(SETTINGS_FILE, 'w+')
    with open(SETTINGS_FILE, 'w+') as f:
        f.write(json.dumps(DEFAULT_SETTINGS))


def readSettingsFile():
    with open(SETTINGS_FILE) as f:
        return json.load(f)


def validateSettings(settings):

    for key in ["checkIsOut", "checkIsColliding"]:
        if not(key in settings.keys()) or (type(settings[key]) != bool):
            return False

    for key in ["canvasSize", "cellNum", "intervalMilliseconds"]:
        if not(key in settings.keys()) or (type(settings[key]) != int) or (settings[key] <= 0):
            return False

    if settings["canvasSize"] < settings["cellNum"]:
        return False

    if settings["canvasSize"] < 10:
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
        createSettingsFile()

    settings = readSettingsFile()

    if not validateSettings(settings):
        print("settings.json is not valid. " +
              "You can delete it and restart the application. " +
              "App will recreate settings file if it's not present")
        sys.exit()

    return settings
