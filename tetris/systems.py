import pygame

from ecs.system import System
from tetris.components import (
    Block,
    GridPosition,
    ActivePiece,
    Falling,
    Rotation,
    PieceType,
    Score,
)
from tetris.pieces import PIECES
from tetris.config import (
    GRID_WIDTH,
    GRID_HEIGHT,
    CELL_SIZE,
    GRID_COLOR,
)


class RenderSystem(System):
    """
    Responsible for drawing the Tetris board and all blocks.
    """

    def __init__(self, screen):
        self.screen = screen

    def update(self, world, dt, events):
        self.draw_grid()
        self.draw_blocks(world)

    def draw_grid(self):
        """
        Draw the Tetris grid.
        """

        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (x * CELL_SIZE, 0),
                (x * CELL_SIZE, GRID_HEIGHT * CELL_SIZE),
            )

        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (0, y * CELL_SIZE),
                (GRID_WIDTH * CELL_SIZE, y * CELL_SIZE),
            )

    def draw_blocks(self, world):
        """
        Draw all block entities.
        """

        for entity, (block, pos) in world.get_entities_with(Block, GridPosition):
            px = pos.x * CELL_SIZE
            py = pos.y * CELL_SIZE

            rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(self.screen, block.color, rect)

            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                rect,
                1,
            )


class GravitySystem(System):
    """
    Moves the active piece downward over time.
    """

    def __init__(self, fall_interval=0.5):
        self.fall_interval = fall_interval
        self.timer = 0

    def update(self, world, dt, events):
        self.timer += dt

        if self.timer < self.fall_interval:
            return

        self.timer = 0

        for entity, (pos, active, falling) in world.get_entities_with(
            GridPosition, ActivePiece, Falling
        ):
            pos.y += 1


class InputSystem(System):
    """
    Handles player input for moving the active piece.
    """

    def update(self, world, dt, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_LEFT:
                self.move(world, dx=-1)

            elif event.key == pygame.K_RIGHT:
                self.move(world, dx=1)

            elif event.key == pygame.K_DOWN:
                self.move(world, dy=1)

            elif event.key == pygame.K_UP:
                self.rotate(world)

    def move(self, world, dx=0, dy=0):
        """
        Move all blocks belonging to the active piece if the movement is valid.
        """
        active_blocks = list(
            world.get_entities_with(GridPosition, ActivePiece, Falling)
        )

        if not active_blocks:
            return

        active_entities = {entity for entity, _ in active_blocks}
        occupied = self.get_occupied_cells(world, active_entities)

        # check if move is valid
        for entity, (pos, active, falling) in active_blocks:
            new_x = pos.x + dx
            new_y = pos.y + dy

            if new_x < 0 or new_x >= GRID_WIDTH:
                return

            if new_y < 0 or new_y >= GRID_HEIGHT:
                return

            if (new_x, new_y) in occupied:
                return

        # apply movement
        for entity, (pos, active, falling) in active_blocks:
            pos.x += dx
            pos.y += dy

    def rotate(self, world):
        """
        Rotate the active tetromino.
        """

        active_blocks = list(
            world.get_entities_with(
                GridPosition, ActivePiece, Falling, Rotation, PieceType
            )
        )

        if not active_blocks:
            return

        # Use first block as pivot
        pivot_entity, (pivot_pos, active, falling, rotation, piece_type) = (
            active_blocks[0]
        )

        piece_data = PIECES[piece_type.name]
        rotations = piece_data["rotations"]

        next_rotation = (rotation.value + 1) % len(rotations)
        offsets = rotations[next_rotation]

        pivot_x = pivot_pos.x
        pivot_y = pivot_pos.y

        active_entities = {entity for entity, _ in active_blocks}
        occupied = self.get_occupied_cells(world, active_entities)

        new_positions = []

        for i, (entity, (pos, active, falling, rot, ptype)) in enumerate(active_blocks):
            dx, dy = offsets[i]

            new_x = pivot_x + dx
            new_y = pivot_y + dy

            if new_x < 0 or new_x >= GRID_WIDTH:
                return

            if new_y < 0 or new_y >= GRID_HEIGHT:
                return

            if (new_x, new_y) in occupied:
                return

            new_positions.append((pos, new_x, new_y))

        # Apply rotation
        for pos, new_x, new_y in new_positions:
            pos.x = new_x
            pos.y = new_y

        # Update rotation state
        for entity, (pos, active, falling, rot, ptype) in active_blocks:
            rot.value = next_rotation

    def get_occupied_cells(self, world, active_entities):
        """
        Return occupied board cells excluding the active piece
        """
        occupied = set()

        for entity, (block, pos) in world.get_entities_with(Block, GridPosition):
            if entity not in active_entities:
                occupied.add((pos.x, pos.y))

        return occupied


class CollisionSystem(System):
    """
    Detects floor/block collisions and locks the active piece
    """

    def update(self, world, dt, events):
        active_blocks = list(
            world.get_entities_with(GridPosition, ActivePiece, Falling)
        )

        if not active_blocks:
            return

        # build a set of occupied board cells (excluding active piece)
        occupied = set()

        for entity, (block, pos) in world.get_entities_with(Block, GridPosition):
            if entity not in [e for e, _ in active_blocks]:
                occupied.add((pos.x, pos.y))

        collision = False

        for entity, (pos, active, falling) in active_blocks:
            next_y = pos.y + 1

            # floor collision
            if next_y >= GRID_HEIGHT:
                collision = True
                break

            # block collision
            if (pos.x, next_y) in occupied:
                collision = True
                break

        if collision:
            self.lock_piece(world, active_blocks)

    def lock_piece(self, world, active_blocks):
        """
        Convert active blocks into static board blocks
        """
        for entity, (pos, active, falling) in active_blocks:
            world.components[ActivePiece].pop(entity, None)
            world.components[Falling].pop(entity, None)


class LineClearSystem(System):
    """
    Detect and clear completed lines, and award score
    """

    def update(self, world, dt, events):
        # do not clear lines while a piece is still falling
        active_piece = list(world.get_entities_with(ActivePiece))
        if active_piece:
            return

        # build row map
        rows = {y: [] for y in range(GRID_HEIGHT)}

        for entity, (block, pos) in world.get_entities_with(Block, GridPosition):
            rows[pos.y].append(entity)

        # find full rows
        full_rows = [y for y, entities in rows.items() if len(entities) == GRID_WIDTH]

        if not full_rows:
            return

        # score calculation
        lines_cleared = len(full_rows)

        score_table = {
            1: 100,
            2: 300,
            3: 500,
            4: 800,
        }

        points = score_table.get(lines_cleared, 0)

        for entity, (score,) in world.get_entities_with(Score):
            score.value += points
            print("Score:", score.value)

        # remove blocks in full rows
        for y in full_rows:
            for entity in rows[y]:
                world.remove_entity(entity)

        # drop blocks above cleared rows
        for entity, (block, pos) in world.get_entities_with(Block, GridPosition):
            drop_amount = sum(1 for row in full_rows if pos.y < row)

            if drop_amount > 0:
                pos.y += drop_amount


class GameOverSystem(System):
    """
    Ends the game if the spawn area is blocked
    """

    def update(self, world, dt, events):
        active_piece = list(world.get_entities_with(ActivePiece))

        # only check when a new piece is about to spawn
        if active_piece:
            return

        occupied = set()

        for entity, (block, pos) in world.get_entities_with(Block, GridPosition):
            occupied.add((pos.x, pos.y))

        spawn_x = GRID_WIDTH // 2

        spawn_cells = [
            (spawn_x, 0),
            (spawn_x - 1, 0),
            (spawn_x + 1, 0),
            (spawn_x, 1),
        ]

        for cell in spawn_cells:
            if cell in occupied:
                print("GAME OVER")
                world.running = False
                return
