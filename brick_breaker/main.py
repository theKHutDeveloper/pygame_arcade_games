import pygame

from ecs.world import World
from brick_breaker.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_COLOUR,
    TITLE,
    FPS,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_COLOUR,
)
from brick_breaker.components import Player, Velocity, Position, Sprite
from brick_breaker.systems.movement_system import MovementSystem
from brick_breaker.systems.player_input_system import PlayerInputSystem
from brick_breaker.systems.render_system import RenderSystem


def create_player(world):
    player = world.create_entity()
    world.add_component(player, Player())

    world.add_component(player, Position(PLAYER_START_X, PLAYER_START_Y))
    world.add_component(player, Velocity(0, 0))
    world.add_component(player, Sprite(PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOUR))


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    world = World()
    create_player(world)

    world.add_system(PlayerInputSystem())
    world.add_system(MovementSystem())
    world.add_system(RenderSystem(screen))

    while world.running:
        dt = clock.tick(FPS) / 1000

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                world.running = False

        screen.fill(BACKGROUND_COLOUR)

        world.update(dt, events)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
