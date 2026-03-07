import pygame

from ecs.world import World


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake ECS Test")

    clock = pygame.time.Clock()
    world = World()
    running = True

    while running:

        dt = clock.tick(60) / 1000
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        world.update(dt, events)
        screen.fill((20, 20, 30))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
