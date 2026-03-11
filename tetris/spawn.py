import random

from ecs.system import System

from tetris.components import (
    GridPosition,
    Block,
    ActivePiece,
    Falling,
    Rotation,
    PieceType,
    GameState,
    NextPiece,
)

from tetris.pieces import PIECES
from tetris.config import GRID_WIDTH


class SpawnSystem(System):
    """
    Spawns a new tetromino when no active piece exists.
    Also maintains the upcoming next piece preview.
    """

    def __init__(self):
        self.piece_counter = 0

    def update(self, world, dt, events):
        # check if game is over, if so, stop
        states = list(world.get_entities_with(GameState))

        if states:
            _, (state,) = states[0]
            if state.state != "playing":
                return

        # Check if an active piece already exists
        active_blocks = list(world.get_entities_with(ActivePiece))

        if active_blocks:
            return

        next_piece_entities = list(world.get_entities_with(NextPiece))

        # If no NextPiece exists yet, create one first
        if not next_piece_entities:
            preview_entity = world.create_entity()
            world.add_component(preview_entity, NextPiece(self.random_piece_name()))
            next_piece_entities = list(world.get_entities_with(NextPiece))

        preview_entity, (next_piece,) = next_piece_entities[0]

        piece_name_to_spawn = next_piece.name

        # Roll and store the next preview piece
        next_piece.name = self.random_piece_name()

        self.spawn_piece(world, piece_name_to_spawn)

    def spawn_piece(self, world, piece_name):
        """
        Create a new tetromino using ECS entities.
        """

        piece_data = PIECES[piece_name]

        rotations = piece_data["rotations"]
        offsets = rotations[0]  # start with first rotation
        color = piece_data["color"]

        spawn_x = GRID_WIDTH // 2
        spawn_y = 0

        self.piece_counter += 1
        piece_id = self.piece_counter

        for dx, dy in offsets:
            entity = world.create_entity()

            world.add_component(entity, GridPosition(spawn_x + dx, spawn_y + dy))
            world.add_component(entity, Block(color))
            world.add_component(entity, ActivePiece(piece_id))
            world.add_component(entity, Falling())
            world.add_component(entity, Rotation(0))
            world.add_component(entity, PieceType(piece_name))

    def random_piece_name(self):
        return random.choice(list(PIECES.keys()))
