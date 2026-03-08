import pygame

from ecs.world import World
from tetris.config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris ECS")

    clock = pygame.time.Clock()

    world = World()

    while world.running:
        dt = clock.tick(60) / 1000

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                world.running = False

        world.update(dt, events)

        screen.fill(BACKGROUND_COLOR)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
