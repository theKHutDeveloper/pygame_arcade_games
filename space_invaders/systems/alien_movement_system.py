from ecs.system import System
from space_invaders.components import Alien, Position, AlienFormation
from space_invaders.config import (
    ALIEN_MOVE_DISTANCE,
    ALIEN_MOVE_DOWN,
    ALIEN_MOVE_INTERVAL,
    SCREEN_WIDTH,
)


class AlienMovementSystem(System):

    def update(self, world, dt, events):

        formations = list(world.get_entities_with(AlienFormation))

        if not formations:
            return

        formation_entity, (formation,) = formations[0]

        formation.move_timer += dt

        if formation.move_timer < ALIEN_MOVE_INTERVAL:
            return

        formation.move_timer = 0

        aliens = list(world.get_entities_with(Alien, Position))

        if not aliens:
            return

        hit_edge = False

        for entity, (alien, pos) in aliens:

            if (
                formation.direction == 1
                and pos.x + ALIEN_MOVE_DISTANCE > SCREEN_WIDTH - 40
            ):
                hit_edge = True

            if formation.direction == -1 and pos.x - ALIEN_MOVE_DISTANCE < 0:
                hit_edge = True

        if hit_edge:

            formation.direction *= -1

            for entity, (alien, pos) in aliens:
                pos.y += ALIEN_MOVE_DOWN

        else:

            for entity, (alien, pos) in aliens:
                pos.x += ALIEN_MOVE_DISTANCE * formation.direction
