from ecs.system import System
from space_invaders.components import Bullet, Position
from space_invaders.config import SCREEN_HEIGHT


class BulletCleanupSystem(System):

    def update(self, world, dt, events):

        bullets = list(world.get_entities_with(Bullet, Position))

        for entity, (bullet, pos) in bullets:

            if pos.y < -20 or pos.y > SCREEN_HEIGHT + 20:
                world.remove_entity(entity)
