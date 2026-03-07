import pygame

import random
from ecs.system import System
from snake.components import GridPosition, SnakeHead, SnakeBody, Direction, Food
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


class FoodSpawnSystem(System):
    def update(self, world, dt, events):
        # check if food already exists
        foods = list(world.get_entities_with(Food, GridPosition))

        if foods:
            return

        # spawn new food
        entity = world.create_entity()

        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)

        world.add_component(entity, Food())
        world.add_component(entity, GridPosition(x, y))


class RenderFoodSystem(System):
    def __init__(self, screen):
        self.screen = screen

    def update(self, world, dt, events):
        for entity, (food, pos) in world.get_entities_with(Food, GridPosition):
            rect = pygame.Rect(
                pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(self.screen, (220, 50, 50), rect)


class FoodEatingSystem(System):
    def update(self, world, dt, events):
        heads = list(world.get_entities_with(SnakeHead, GridPosition))
        foods = list(world.get_entities_with(Food, GridPosition))

        if not heads or not foods:
            return

        head_entity, (head, head_pos) = heads[0]

        for food_entity, (food, food_pos) in foods:
            if head_pos.x == food_pos.x and head_pos.y == food_pos.y:
                world.remove_entity(food_entity)
