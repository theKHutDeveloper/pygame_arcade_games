import pygame

from ecs.system import System
from space_invaders.components import GameState, Alien


class GameStateSystem(System):

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 72)

    def update(self, world, dt, events):

        states = list(world.get_entities_with(GameState))

        if not states:
            return

        _, (state,) = states[0]

        aliens = list(world.get_entities_with(Alien))

        if state.state == "playing" and not aliens:
            state.state = "victory"

        if state.state == "game_over":

            text = self.font.render("GAME OVER", True, (255, 50, 50))
            rect = text.get_rect(center=(400, 300))
            self.screen.blit(text, rect)

        if state.state == "victory":

            text = self.font.render("VICTORY", True, (50, 255, 50))
            rect = text.get_rect(center=(400, 300))
            self.screen.blit(text, rect)
