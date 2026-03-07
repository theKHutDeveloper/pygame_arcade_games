from dataclasses import dataclass


@dataclass
class GridPosition:
    x: int
    y: int


@dataclass
class Direction:
    x: int
    y: int


@dataclass
class SnakeHead:
    pass


@dataclass
class SnakeBody:
    order: int


@dataclass
class Food:
    pass


@dataclass
class Grow:
    amount: int = 1
