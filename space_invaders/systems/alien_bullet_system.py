import random

from ecs.system import System
from space_invaders.components import (
    Alien,
    Position,
    Sprite,
    Bullet,
    Velocity,
    Collider,
)
from space_invaders.config import (
    BULLET_WIDTH,
    BULLET_HEIGHT,
    ALIEN_BULLET_COLOUR,
    BULLET_SPEED,
)


class AlienBulletSystem(System):

    def __init__(self):
        self.timer = 0
        self.fire_interval = 1.0

    def update(self, world, dt, events):

        self.timer += dt

        if self.timer < self.fire_interval:
            return

        self.timer = 0

        aliens = list(world.get_entities_with(Alien, Position, Sprite))

        if not aliens:
            return

        shooter_entity, (alien, pos, sprite) = random.choice(aliens)

        bullet = world.create_entity()

        bullet_x = pos.x + sprite.width / 2 - BULLET_WIDTH / 2
        bullet_y = pos.y + sprite.height

        world.add_component(bullet, Position(bullet_x, bullet_y))

        world.add_component(bullet, Velocity(0, BULLET_SPEED))

        world.add_component(
            bullet,
            Sprite(
                BULLET_WIDTH,
                BULLET_HEIGHT,
                ALIEN_BULLET_COLOUR,
            ),
        )

        world.add_component(bullet, Bullet("alien"))

        world.add_component(
            bullet,
            Collider(
                BULLET_WIDTH,
                BULLET_HEIGHT,
            ),
        )
