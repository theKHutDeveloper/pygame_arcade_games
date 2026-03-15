import pygame

from ecs.system import System
from brick_breaker.components import Position, Sprite


class RenderSystem(System):
    def __init__(self, screen):
        self.screen = screen

    def update(self, world, dt, events):
        for entity, (pos, sprite) in world.get_entities_with(Position, Sprite):
            rect = pygame.Rect(
                int(pos.x),
                int(pos.y),
                sprite.width,
                sprite.height,
            )

            pygame.draw.rect(self.screen, sprite.colour, rect)
