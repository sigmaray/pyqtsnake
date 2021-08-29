from munch import Munch

CELL_TYPES = Munch()
CELL_TYPES.empty = "empty"
CELL_TYPES.food = "food"
CELL_TYPES.snakeSegment = "snakeSegment"
CELL_TYPES.snakeHead = "snakeHead"

COLORS = Munch()
COLORS.snakeSegment = "Olive"
COLORS.snakeHead = "Green"
COLORS.food = "red"

DEFAULT_SETTINGS = {
    "cellNum": 15,
    "intervalMilliseconds": 150,
    "checkIsOut": False,
    "checkIsColliding": False,
}

SETTINGS_FILE = "settings.json"

