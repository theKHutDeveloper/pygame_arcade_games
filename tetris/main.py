import pygame

from ecs.world import World
from tetris.config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from tetris.systems import (
    RenderSystem,
    GravitySystem,
    InputSystem,
    CollisionSystem,
    LineClearSystem,
    GameOverSystem,
    RenderScoreSystem,
    GameOverRenderSystem,
    RestartSystem,
)
from tetris.spawn import SpawnSystem
from tetris.components import Score, GameState


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris ECS")

    clock = pygame.time.Clock()

    world = World()

    game_entity = world.create_entity()

    world.add_component(game_entity, Score(0))
    world.add_component(game_entity, GameState("playing"))

    world.add_system(LineClearSystem())
    world.add_system(GameOverSystem())
    world.add_system(RestartSystem())
    world.add_system(SpawnSystem())
    world.add_system(InputSystem())
    world.add_system(GravitySystem())
    world.add_system(CollisionSystem())
    world.add_system(RenderSystem(screen))
    world.add_system(RenderScoreSystem(screen))
    world.add_system(GameOverRenderSystem(screen))

    while world.running:
        dt = clock.tick(60) / 1000

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                world.running = False

        screen.fill(BACKGROUND_COLOR)

        world.update(dt, events)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
