"""Constants and enums used in Snake."""
from enum import Enum
import type_declarations as t


class CHECKBOX_COLORS(str, Enum):
    """Colors that should be used for checkboxes."""

    empty = "#fff"
    snakeSegment = "Olive"
    snakeHead = "Green"
    food = "Red"

    def __str__(self) -> str:
        """Make it possible to write ENUM.field instead of ENUM.field.value."""
        return str.__str__(self)


class CANVAS_COLORS(str, Enum):
    """Colors that should be used in canvas."""

    emptyBackground = "GhostWhite"
    snakeSegmentBackground = "ForestGreen"
    snakeHeadBackground = "Chartreuse"
    foodBackground = "Red"
    border = "Black"

    def __str__(self) -> str:
        """Make it possible to write ENUM.field instead of ENUM.field.value."""
        return str.__str__(self)


DEFAULT_SETTINGS = t.Settings(
    cellNum=5,
    intervalMilliseconds=150,
    cellSize=30,
    checkIsOut=False,
    checkIsColliding=False,
    disableTimer=False
)

SETTINGS_FILE = "settings.json"
