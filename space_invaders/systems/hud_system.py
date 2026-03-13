import pygame

from ecs.system import System
from space_invaders.components import Score, Lives


class HUDSystem(System):

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 28)

    def update(self, world, dt, events):

        scores = list(world.get_entities_with(Score))
        lives_entities = list(world.get_entities_with(Lives))

        score_value = scores[0][1][0].value if scores else 0
        lives_value = lives_entities[0][1][0].value if lives_entities else 0

        score_text = self.font.render(f"Score: {score_value}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {lives_value}", True, (255, 255, 255))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
