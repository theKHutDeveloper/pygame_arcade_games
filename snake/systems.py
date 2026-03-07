import pygame

from ecs.system import System
from snake.components import GridPosition, SnakeHead, SnakeBody, Direction
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


class SnakeMovementSystem(System):
    def update(self, world, dt, events):
        # get the snake head
        head_data = list(world.get_entities_with(SnakeHead, GridPosition, Direction))

        if not head_data:
            return

        head_entity, (head, head_pos, direction) = head_data[0]

        # collect body segments
        body_segments = []

        for entity, (body, pos) in world.get_entities_with(SnakeBody, GridPosition):
            body_segments.append((body.order, pos))

        # sort body segments so they follow correctly
        body_segments.sort(key=lambda x: x[0])

        # store previous positions
        previous_positions = [(head_pos.x, head_pos.y)]

        for _, pos in body_segments:
            previous_positions.append((pos.x, pos.y))

        # move head
        head_pos.x += direction.x
        head_pos.y += direction.y

        # move body segments
        for i, (_, pos) in enumerate(body_segments):
            pos.x, pos.y = previous_positions[i]
