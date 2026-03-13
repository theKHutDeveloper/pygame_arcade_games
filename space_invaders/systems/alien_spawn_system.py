from ecs.system import System
from space_invaders.components import Alien, Position, Sprite, Collider, AlienFormation
from space_invaders.config import (
    ALIEN_ROWS,
    ALIEN_COLS,
    ALIEN_WIDTH,
    ALIEN_HEIGHT,
    ALIEN_COLOUR,
    ALIEN_HORIZONTAL_SPACING,
    ALIEN_VERTICAL_SPACING,
    ALIEN_START_X,
    ALIEN_START_Y,
)


class AlienSpawnSystem(System):

    def __init__(self):
        self.spawned = False

    def update(self, world, dt, events):

        if self.spawned:
            return

        formation = world.create_entity()

        world.add_component(
            formation,
            AlienFormation(
                1,
                0,
            ),
        )

        for row in range(ALIEN_ROWS):

            for col in range(ALIEN_COLS):

                alien = world.create_entity()

                x = ALIEN_START_X + col * (ALIEN_WIDTH + ALIEN_HORIZONTAL_SPACING)
                y = ALIEN_START_Y + row * (ALIEN_HEIGHT + ALIEN_VERTICAL_SPACING)

                world.add_component(alien, Alien(row, col))

                world.add_component(alien, Position(x, y))

                world.add_component(
                    alien,
                    Sprite(
                        ALIEN_WIDTH,
                        ALIEN_HEIGHT,
                        ALIEN_COLOUR,
                    ),
                )

                world.add_component(
                    alien,
                    Collider(
                        ALIEN_WIDTH,
                        ALIEN_HEIGHT,
                    ),
                )

        self.spawned = True
