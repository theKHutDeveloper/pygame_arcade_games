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
class Alien:
    row: int
    col: int


@dataclass
class Bullet:
    owner: str  # "player" or "alien"


@dataclass
class Collider:
    width: int
    height: int


@dataclass
class Health:
    current: int


@dataclass
class Score:
    value: int


@dataclass
class Lives:
    value: int


@dataclass
class FireCooldown:
    time_left: float
    delay: float


@dataclass
class AlienFormation:
    direction: int  # 1 for right, -1 for left
    move_timer: float


@dataclass
class GameState:
    state: str  # "playing", "game_over", "victory"
