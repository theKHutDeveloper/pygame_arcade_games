from dataclasses import dataclass


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Velocity:
    x: float
    y: float


@dataclass
class Sprite:
    width: int
    height: int
    colour: tuple[int, int, int]


@dataclass
class Player:
    pass


@dataclass
class GameState:
    state: str  # "playing", "game_over", "victory"
