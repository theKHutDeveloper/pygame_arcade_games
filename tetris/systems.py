import pygame

from ecs.system import System
from tetris.components import Block, GridPosition
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
