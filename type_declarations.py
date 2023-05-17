"""Types for snake game."""
# pylint: disable=missing-class-docstring
from dataclasses import dataclass
from typing import List, Literal
from enum import Enum


@dataclass
class Coordinate:
    """Coordinate of snake segment/snake head/food."""

    x: int
    y: int


@dataclass
class State:
    """State of the game."""

    snakeDirection: Literal["up", "down", "left", "right"]
    isPaused: bool
    snakeSegments: List[Coordinate]
    food: Coordinate
    switchingDirection: bool


class CellTypes(str, Enum):
    """Types of board cell."""

    empty = 'empty'
    food = 'food'
    snakeSegment = 'snakeSegment'
    snakeHead = 'snakeHead'

    def __str__(self) -> str:
        """Make it possible to write ENUM.field instead of ENUM.field.value."""
        return str.__str__(self)


CellType = Literal[CellTypes.empty, CellTypes.food, CellTypes.snakeSegment, CellTypes.snakeHead]


@dataclass
class Settings:
    """Game settings."""

    cellNum: int
    intervalMilliseconds: int
    checkIsOut: bool
    checkIsColliding: bool
