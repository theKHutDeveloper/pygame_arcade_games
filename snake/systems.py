import pygame

import random
from ecs.system import System
from snake.components import GridPosition, SnakeHead, SnakeBody, Direction, Food, Grow
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

        body_entities = []
        body_segments = []

        for entity, (body, pos) in world.get_entities_with(SnakeBody, GridPosition):
            body_entities.append(entity)
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

        # move body
        for i, (_, pos) in enumerate(body_segments):
            pos.x, pos.y = previous_positions[i]

        # check for grow component
        grows = list(world.get_entities_with(Grow))

        for entity, (grow,) in grows:
            if entity == head_entity:
                # new body position is last previous position
                x, y = previous_positions[-1]
                new_body = world.create_entity()

                world.add_component(new_body, SnakeBody(order=len(body_segments)))
                world.add_component(new_body, GridPosition(x, y))

                # remove grow component
                world.components[Grow].pop(head_entity, None)


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
                # remove the food
                world.remove_entity(food_entity)

                # tell the snake to grow
                world.add_component(head_entity, Grow(1))


class SnakeWallCollisionSystem(System):
    def update(self, world, dt, events):
        heads = list(world.get_entities_with(SnakeHead, GridPosition))

        if not heads:
            return

        head_entity, (head, pos) = heads[0]

        if pos.x < 0 or pos.x >= GRID_WIDTH or pos.y < 0 or pos.y >= GRID_HEIGHT:
            print("Game Over: Hit wall")
            world.running = False


class SnakeSelfCollisionSystem(System):
    def update(self, world, dt, events):
        heads = list(world.get_entities_with(SnakeHead, GridPosition))
        bodies = list(world.get_entities_with(SnakeBody, GridPosition))

        if not heads:
            return

        head_entity, (head, head_pos) = heads[0]

        for entity, (body, body_pos) in bodies:
            if head_pos.x == body_pos.x and head_pos.y == body_pos.y:
                print("Game Over: Hit yourself")
                world.running = False
                return


class SnakeInputSystem(System):
    def update(self, world, dt, events):
        heads = list(world.get_entities_with(SnakeHead, Direction))

        if not heads:
            return

        head_entity, (head, direction) = heads[0]

        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            # UP
            if event.key in (pygame.K_UP, pygame.K_w):
                if direction.y != 1:
                    direction.x = 0
                    direction.y = -1

            # DOWN
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if direction.y != -1:
                    direction.x = 0
                    direction.y = 1

            # LEFT
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if direction.x != 1:
                    direction.x = -1
                    direction.y = 0

            # RIGHT
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if direction.x != -1:
                    direction.x = 1
                    direction.y = 0
