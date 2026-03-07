from snake.components import GridPosition, Direction, SnakeHead, SnakeBody


def spawn_snake(world):
    """Create a snake with a head and two body segments"""

    # head
    head = world.create_entity()

    world.add_component(head, SnakeHead())
    world.add_component(head, GridPosition(10, 10))
    world.add_component(head, Direction(1, 0))

    # body segment 1
    body1 = world.create_entity()

    world.add_component(body1, SnakeBody(order=0))
    world.add_component(body1, GridPosition(9, 10))

    # body segment 2
    body2 = world.create_entity()

    world.add_component(body2, SnakeBody(order=1))
    world.add_component(body2, GridPosition(8, 10))
