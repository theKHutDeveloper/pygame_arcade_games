from ecs.system import System
from space_invaders.components import (
    Bullet,
    Alien,
    Player,
    Position,
    Collider,
    Score,
    Lives,
    GameState,
)
from space_invaders.config import PLAYER_START_X, PLAYER_START_Y


class CollisionSystem(System):

    def update(self, world, dt, events):

        bullets = list(world.get_entities_with(Bullet, Position, Collider))
        aliens = list(world.get_entities_with(Alien, Position, Collider))
        players = list(world.get_entities_with(Player, Position, Collider))
        scores = list(world.get_entities_with(Score))
        lives_entities = list(world.get_entities_with(Lives))

        score = scores[0][1][0] if scores else None
        lives = lives_entities[0][1][0] if lives_entities else None

        bullets_to_remove = []
        aliens_to_remove = []

        # --- bullet vs alien ---
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

        # --- alien bullet vs player ---
        for bullet_entity, (bullet, bullet_pos, bullet_col) in bullets:

            if bullet.owner != "alien":
                continue

            for player_entity, (player, player_pos, player_col) in players:

                if (
                    bullet_pos.x < player_pos.x + player_col.width
                    and bullet_pos.x + bullet_col.width > player_pos.x
                    and bullet_pos.y < player_pos.y + player_col.height
                    and bullet_pos.y + bullet_col.height > player_pos.y
                ):

                    bullets_to_remove.append(bullet_entity)

                    if lives:
                        lives.value -= 1
                        print("PLAYER HIT! - Lives: ", lives.value)

                    if lives and lives.value <= 0:
                        states = list(world.get_entities_with(GameState))

                        if states:
                            _, (state,) = states[0]
                            state.state = "game_over"

                    player_pos.x = PLAYER_START_X
                    player_pos.y = PLAYER_START_Y

        for entity in bullets_to_remove:
            world.remove_entity(entity)

        for entity in aliens_to_remove:
            world.remove_entity(entity)
