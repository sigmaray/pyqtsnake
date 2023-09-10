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

    emptyBackground = "#ccc"
    snakeSegmentBackground = "Green"
    snakeHeadBackground = "Blue"
    foodBackground = "Red"
    border = "SlateBlue"

    def __str__(self) -> str:
        """Make it possible to write ENUM.field instead of ENUM.field.value."""
        return str.__str__(self)


DEFAULT_SETTINGS = t.Settings(
    cellNum=15,
    intervalMilliseconds=150,
    checkIsOut=False,
    checkIsColliding=False,
    disableTimer=False
)

SETTINGS_FILE = "settings.json"
