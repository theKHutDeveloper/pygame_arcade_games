import pygame

from ecs.system import System
from brick_breaker.components import Player, Velocity
from brick_breaker.config import PLAYER_SPEED


class PlayerInputSystem(System):
    def update(self, world, dt, events):
        keys = pygame.key.get_pressed()

        for entity, (player, velocity) in world.get_entities_with(Player, Velocity):
            velocity.x = 0

            if keys[pygame.K_LEFT]:
                velocity.x = -PLAYER_SPEED

            if keys[pygame.K_RIGHT]:
                velocity.x = PLAYER_SPEED
