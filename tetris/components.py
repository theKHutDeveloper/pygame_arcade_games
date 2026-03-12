from dataclasses import dataclass


@dataclass
class GridPosition:
    """
    Grid coordinate of a block.

    Example:
        x=5, y=10 means column 5, row 10
    """

    x: int
    y: int


@dataclass
class Block:
    """
    Marks an entity as a Tetris block.
    """

    color: tuple[int, int, int]


@dataclass
class ActivePiece:
    """
    Marks blocks belonging to the currently falling piece.

    All blocks with this component move together.
    """

    piece_id: int


@dataclass
class Falling:
    """
    Marker component that indicates the piece is falling.
    """

    pass


@dataclass
class Rotation:
    """
    Stores the current rotation index of the piece.
    """

    value: int = 0


@dataclass
class PieceType:
    """
    Stores the tetromino type (I, O, T, etc).
    """

    name: str


@dataclass
class Score:
    value: int = 0


@dataclass
class GameState:
    state: str


@dataclass
class NextPiece:
    name: str


@dataclass
class GhostBlock:
    """
    Marker for ghost piece blocks.
    """

    pass
