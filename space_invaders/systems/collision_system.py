from ecs.system import System
from space_invaders.components import Bullet, Alien, Position, Collider, Score


class CollisionSystem(System):

    def update(self, world, dt, events):

        bullets = list(world.get_entities_with(Bullet, Position, Collider))
        aliens = list(world.get_entities_with(Alien, Position, Collider))
        scores = list(world.get_entities_with(Score))

        if scores:
            score_entity, (score,) = scores[0]
        else:
            score = None

        bullets_to_remove = []
        aliens_to_remove = []

        for bullet_entity, (bullet, bullet_pos, bullet_col) in bullets:

            if bullet.owner != "player":
                continue

            for alien_entity, (alien, alien_pos, alien_col) in aliens:

                if (
                    bullet_pos.x < alien_pos.x + alien_col.width
                    and bullet_pos.x + bullet_col.width > alien_pos.x
                    and bullet_pos.y < alien_pos.y + alien_col.height
                    and bullet_pos.y + bullet_col.height > alien_pos.y
                ):

                    bullets_to_remove.append(bullet_entity)
                    aliens_to_remove.append(alien_entity)

                    if score:
                        score.value += 10

        for entity in bullets_to_remove:
            world.remove_entity(entity)

        for entity in aliens_to_remove:
            world.remove_entity(entity)
