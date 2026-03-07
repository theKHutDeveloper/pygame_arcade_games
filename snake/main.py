import pygame

from ecs.world import World
from snake.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from snake.systems import RenderGridSystem, RenderSnakeSystem
from snake.spawn import spawn_snake


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake ECS")

    clock = pygame.time.Clock()

    world = World()

    spawn_snake(world)

    world.add_system(RenderGridSystem(screen))
    world.add_system(RenderSnakeSystem(screen))

    running = True

    while running:

        dt = clock.tick(FPS) / 1000.0
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        world.update(dt, events)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
