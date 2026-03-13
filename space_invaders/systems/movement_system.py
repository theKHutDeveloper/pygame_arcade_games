from ecs.system import System
from space_invaders.components import Position, Velocity


class MovementSystem(System):
    def update(self, world, dt, events):
        for entity, (pos, vel) in world.get_entities_with(Position, Velocity):
            pos.x += vel.x * dt
            pos.y += vel.y * dt
