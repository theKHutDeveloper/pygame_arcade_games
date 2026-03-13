import pygame

from ecs.world import World
from space_invaders.components import GameState, Score, Lives
from space_invaders.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE,
    BACKGROUND_COLOUR,
    PLAYER_LIVES,
)


def create_initial_entities(world):
    ui_entity = world.create_entity()
    world.add_component(ui_entity, Score(0))
    world.add_component(ui_entity, Lives(PLAYER_LIVES))

    state_entity = world.create_entity()
    world.add_component(state_entity, GameState("playing"))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    world = World()
    create_initial_entities(world)

    while world.running:
        dt = clock.tick(FPS) / 1000
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                world.running = False

        world.update(dt, events)

        screen.fill(BACKGROUND_COLOUR)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
