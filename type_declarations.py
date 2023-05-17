"""Types for snake game"""
# pylint: disable=missing-class-docstring
from dataclasses import dataclass
from typing import List, Literal
from enum import Enum


@dataclass
class Coordinate:
    x: int
    y: int


@dataclass
class State:
    snakeDirection: Literal["up", "down", "left", "right"]
    isPaused: bool
    snakeSegments: List[Coordinate]
    food: Coordinate
    switchingDirection: bool


class CellTypes(str, Enum):
    empty = 'empty'
    food = 'food'
    snakeSegment = 'snakeSegment'
    snakeHead = 'snakeHead'

    def __str__(self) -> str:
        return str.__str__(self)


CellType = Literal[CellTypes.empty, CellTypes.food, CellTypes.snakeSegment, CellTypes.snakeHead]


@dataclass
class Settings:
    cellNum: int
    intervalMilliseconds: int
    checkIsOut: bool
    checkIsColliding: bool
