import pygame

from ecs.system import System
from tetris.components import (
    Block,
    GridPosition,
    ActivePiece,
    Falling,
    Rotation,
    PieceType,
)
from tetris.pieces import PIECES
from tetris.config import (
    GRID_WIDTH,
    GRID_HEIGHT,
    CELL_SIZE,
    GRID_COLOR,
)


class RenderSystem(System):
    """
    Responsible for drawing the Tetris board and all blocks.
    """

    def __init__(self, screen):
        self.screen = screen

    def update(self, world, dt, events):
        self.draw_grid()
        self.draw_blocks(world)

    def draw_grid(self):
        """
        Draw the Tetris grid.
        """

        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (x * CELL_SIZE, 0),
                (x * CELL_SIZE, GRID_HEIGHT * CELL_SIZE),
            )

        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (0, y * CELL_SIZE),
                (GRID_WIDTH * CELL_SIZE, y * CELL_SIZE),
            )

    def draw_blocks(self, world):
        """
        Draw all block entities.
        """

        for entity, (block, pos) in world.get_entities_with(Block, GridPosition):
            px = pos.x * CELL_SIZE
            py = pos.y * CELL_SIZE

            rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(self.screen, block.color, rect)

            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                rect,
                1,
            )


class GravitySystem(System):
    """
    Moves the active piece downward over time.
    """

    def __init__(self, fall_interval=0.5):
        self.fall_interval = fall_interval
        self.timer = 0

    def update(self, world, dt, events):
        self.timer += dt

        if self.timer < self.fall_interval:
            return

        self.timer = 0

        for entity, (pos, active, falling) in world.get_entities_with(
            GridPosition, ActivePiece, Falling
        ):
            pos.y += 1


class InputSystem(System):
    """
    Handles player input for moving the active piece.
    """

    def update(self, world, dt, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_LEFT:
                self.move(world, dx=-1)

            elif event.key == pygame.K_RIGHT:
                self.move(world, dx=1)

            elif event.key == pygame.K_DOWN:
                self.move(world, dy=1)

            elif event.key == pygame.K_UP:
                self.rotate(world)

    def move(self, world, dx=0, dy=0):
        """
        Move all blocks belonging to the active piece.
        """

        for entity, (pos, active, falling) in world.get_entities_with(
            GridPosition, ActivePiece, Falling
        ):
            pos.x += dx
            pos.y += dy

    def rotate(self, world):
        """
        Rotate the active tetromino.
        """

        active_blocks = list(
            world.get_entities_with(
                GridPosition, ActivePiece, Falling, Rotation, PieceType
            )
        )

        if not active_blocks:
            return

        # Use the first block as the pivot
        pivot_entity, (pivot_pos, active, falling, rotation, piece_type) = (
            active_blocks[0]
        )

        piece_data = PIECES[piece_type.name]
        rotations = piece_data["rotations"]

        next_rotation = (rotation.value + 1) % len(rotations)
        offsets = rotations[next_rotation]

        pivot_x = pivot_pos.x
        pivot_y = pivot_pos.y

        # Update positions of all blocks
        for i, (entity, (pos, active, falling, rot, ptype)) in enumerate(active_blocks):
            dx, dy = offsets[i]

            pos.x = pivot_x + dx
            pos.y = pivot_y + dy

            rot.value = next_rotation
