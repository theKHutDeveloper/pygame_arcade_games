import pygame

from ecs.system import System
from snake.components import GridPosition, SnakeHead, SnakeBody
from snake.config import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE


class RenderGridSystem(System):
    def __init__(self, screen):
        self.screen = screen

    def update(self, world, dt, events):
        """Draw the background grid"""

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)


class RenderSnakeSystem(System):
    def __init__(self, screen):
        self.screen = screen

    def update(self, world, dt, events):
        # draw head
        for entity, (head, pos) in world.get_entities_with(SnakeHead, GridPosition):
            rect = pygame.Rect(
                pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )

            pygame.draw.rect(self.screen, (0, 200, 0), rect)

        # draw snake body
        for entity, (body, pos) in world.get_entities_with(SnakeBody, GridPosition):
            rect = pygame.Rect(
                pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )

            pygame.draw.rect(self.screen, (0, 120, 0), rect)
