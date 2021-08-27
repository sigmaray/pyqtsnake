from munch import Munch
# SETTINGS_STORAGE_KEY = "JSSnakeSettings";

CELL_TYPES = Munch()
CELL_TYPES.empty = "empty"
CELL_TYPES.food = "food"
CELL_TYPES.snakeSegment = "snakeSegment"
CELL_TYPES.snakeHead = "snakeHead"

COLORS = Munch()
COLORS.snakeSegment = "Olive"
COLORS.snakeHead = "Green"
# COLORS.segmentBorder = "SlateBlue"
# COLORS.food = "#DDA0DD"
COLORS.food = "red"
COLORS.text = "SlateBlue"
COLORS.canvasColor = "#fff"

DEFAULT_SETTINGS = {
    "canvasSize": 500,
    "cellNum": 15,
    "intervalMilliseconds": 150,
    "checkIsOut": False,
    "checkIsColliding": False,
}

SETTINGS_FILE = "settings.json"

