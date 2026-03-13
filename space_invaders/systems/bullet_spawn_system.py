import pygame

from ecs.system import System
from space_invaders.components import (
    Player,
    Position,
    Bullet,
    Velocity,
    Sprite,
    FireCooldown,
)
from space_invaders.config import (
    BULLET_WIDTH,
    BULLET_HEIGHT,
    BULLET_COLOUR,
    BULLET_SPEED,
)


class BulletSpawnSystem(System):
    def update(self, world, dt, events):
        keys = pygame.key.get_pressed()

        for entity, (player, pos, cooldown) in world.get_entities_with(
            Player, Position, FireCooldown
        ):
            cooldown.time_left -= dt

            if keys[pygame.K_SPACE] and cooldown.time_left <= 0:
                bullet = world.create_entity()

                world.add_component(bullet, Position(pos.x + 2, pos.y))
                world.add_component(bullet, Velocity(0, -BULLET_SPEED))
                world.add_component(
                    bullet, Sprite(BULLET_WIDTH, BULLET_HEIGHT, BULLET_COLOUR)
                )
                world.add_component(bullet, Bullet("player"))

                cooldown.time_left = cooldown.delay
