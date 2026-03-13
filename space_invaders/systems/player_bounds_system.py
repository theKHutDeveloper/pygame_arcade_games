from ecs.system import System
from space_invaders.components import Player, Position, Sprite
from space_invaders.config import SCREEN_WIDTH


class PlayerBoundsSystem(System):
    def update(self, world, dt, events):
        for entity, (player, pos, sprite) in world.get_entities_with(
            Player, Position, Sprite
        ):
            if pos.x < 0:
                pos.x = 0

            if pos.x + sprite.width > SCREEN_WIDTH:
                pos.x = SCREEN_WIDTH - sprite.width
