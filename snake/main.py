import pygame

from ecs.world import World
from snake.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from snake.systems import (
    RenderGridSystem,
    RenderSnakeSystem,
    SnakeMovementSystem,
    FoodSpawnSystem,
    FoodEatingSystem,
    RenderFoodSystem,
    SnakeWallCollisionSystem,
    SnakeSelfCollisionSystem,
    SnakeInputSystem,
    RestartSystem,
    RenderScoreSystem,
    RenderGameStateSystem,
    DebugRenderSystem,
)
from snake.spawn import spawn_snake
from snake.components import Score, GameState


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake ECS")

    clock = pygame.time.Clock()

    world = World()

    # game state entity
    game_entity = world.create_entity()
    world.add_component(game_entity, Score(0))
    world.add_component(game_entity, GameState("playing"))
    spawn_snake(world)

    world.add_system(SnakeInputSystem())
    world.add_system(SnakeMovementSystem())
    world.add_system(SnakeWallCollisionSystem())
    world.add_system(SnakeSelfCollisionSystem())
    world.add_system(FoodEatingSystem())
    world.add_system(FoodSpawnSystem())

    world.add_system(RenderGridSystem(screen))
    world.add_system(RenderFoodSystem(screen))
    world.add_system(RenderSnakeSystem(screen))
    world.add_system(RenderScoreSystem(screen))
    world.add_system(RenderGameStateSystem(screen))

    world.add_system(DebugRenderSystem(screen, clock))

    world.add_system(RestartSystem())

    _ = world.running

    while world.running:

        dt = clock.tick(FPS) / 1000.0
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                world.running = False

        screen.fill((30, 30, 30))

        world.update(dt, events)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
