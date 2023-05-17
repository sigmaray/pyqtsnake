"""Constants and enums used in Snake"""
# pylint: disable=missing-class-docstring
from enum import Enum
import type_declarations as t


class CHECKBOX_COLORS(str, Enum):
    snakeSegment = "Olive"
    snakeHead = "Green"
    food = "red"

    def __str__(self) -> str:
        return str.__str__(self)


class CANVAS_COLORS(str, Enum):
    emptyBackground = "#ccc"
    snakeSegmentBackground = "green"
    snakeHeadBackground = "blue"
    foodBackground = "red"
    border = "SlateBlue"

    def __str__(self) -> str:
        return str.__str__(self)


DEFAULT_SETTINGS = t.Settings(
    cellNum=15,
    intervalMilliseconds=150,
    checkIsOut=False,
    checkIsColliding=False,
)

SETTINGS_FILE = "settings.json"
