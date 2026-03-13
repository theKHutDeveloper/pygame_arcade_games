import pygame

from ecs.world import World
from space_invaders.components import (
    GameState,
    Score,
    Lives,
    Position,
    Sprite,
    Player,
    Velocity,
    FireCooldown,
)
from space_invaders.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE,
    BACKGROUND_COLOUR,
    PLAYER_LIVES,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_COLOUR,
)
from space_invaders.systems.render_system import RenderSystem
from space_invaders.systems.player_input_system import PlayerInputSystem
from space_invaders.systems.movement_system import MovementSystem
from space_invaders.systems.bullet_spawn_system import BulletSpawnSystem


def create_initial_entities(world):
    ui_entity = world.create_entity()
    world.add_component(ui_entity, Score(0))
    world.add_component(ui_entity, Lives(PLAYER_LIVES))

    state_entity = world.create_entity()
    world.add_component(state_entity, GameState("playing"))


def create_player(world):
    player = world.create_entity()

    world.add_component(player, Player())

    world.add_component(
        player,
        Position(
            PLAYER_START_X,
            PLAYER_START_Y,
        ),
    )

    world.add_component(player, Velocity(0, 0))

    world.add_component(
        player,
        Sprite(
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            PLAYER_COLOUR,
        ),
    )

    world.add_component(player, FireCooldown(0, 0.35))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    world = World()
    create_initial_entities(world)
    create_player(world)

    world.add_system(PlayerInputSystem())
    world.add_system(BulletSpawnSystem())
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
