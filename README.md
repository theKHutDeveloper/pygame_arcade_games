# PyGame Arcade Games (ECS)

A collection of classic arcade games implemented in Python using pygame-ce and an Entity Component System (ECS) architecture.

## The purpose of this project is to:

- Practice Python game development

- Learn and apply Entity Component System architecture

- Build a reusable lightweight ECS engine

- Implement multiple classic arcade games using the same engine

Each game lives in its own folder but shares the common ECS framework.

## Project Goals

This project focuses on:

- Learning ECS architecture in practice

- Building reusable systems and components

- Creating small, complete arcade games

- Understanding how game engines structure logic

Rather than building one large game, this repository contains many small arcade games, each demonstrating different mechanics.

## Technologies Used

- Python 3

- pygame-ce

- Custom ECS engine

- Flake8 for linting

- Black for formatting

- pre-commit for automated checks

## Project Structure
```
pygame_arcade_games
│
├── ecs/                # Reusable ECS engine
│   ├── world.py
│   ├── entity.py
│   └── system.py
│
├── snake/              # Snake game implementation
│   └── main.py
│
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

The ecs folder acts as a mini-game engine used by all games in the repository.

## Entity Component System (ECS)

The project uses a simplified ECS architecture.

### Entities

Entities are simple integer IDs.
```
Example:

1
2
3
```
Entities have no behaviour.

### Components

Components contain data only.
```
Example components:

Position
Velocity
GridPosition
Direction
Sprite
SnakeHead
SnakeBody
Food
```

### Systems

Systems contain all game logic.

```
Examples:

MovementSystem
InputSystem
CollisionSystem
RenderSystem
SnakeMovementSystem
MatchDetectionSystem
```
Systems operate on entities that contain specific components.
```
Example:

for entity, (pos, vel) in world.get_entities_with(Position, Velocity):
    pos.x += vel.dx
    pos.y += vel.dy
```

## Planned Arcade Games

The repository will contain multiple classic arcade games implemented using the ECS framework.

### Snake

#### Classic grid-based snake game.

Features:

- Grid movement

- Snake body growth

- Food spawning

- Collision detection

- Score tracking

#### Concepts demonstrated:

- Grid-based ECS

- Multi-entity characters

- Game state management



### Tetris

#### Classic falling block puzzle game.

Features:

- Tetromino shapes

- Piece rotation

- Line clearing

- Scoring system

#### Concepts demonstrated:

- Grid systems

- Spatial transformations

- Board state management



### Match-3

#### Puzzle game similar to Bejeweled.

Features:

- Tile swapping

- Match detection

- Gravity mechanics

- Chain reactions

#### Concepts demonstrated:

- Pattern detection

- board simulation

- cascading updates



### Brick Breaker

#### Arcade paddle game.

Features:

- Ball physics

- Brick destruction

- Paddle control

- Score system

#### Concepts demonstrated:

- Collision systems

- Physics simulation

- Entity removal



### Space Invaders

#### Classic alien shooter.

Features:

- Enemy waves

- Player shooting

- Projectile systems

- Score tracking

#### Concepts demonstrated:

- projectile entities

- enemy AI

- spawning systems



### Asteroids

#### Classic space arcade shooter.

Features:

- Ship rotation

- asteroid splitting

- bullet systems

- wrap-around map

#### Concepts demonstrated:

- vector movement

- physics systems

- entity fragmentation



### Pac-Man (Simplified)

#### Maze-based arcade game.

Features:

- maze navigation

- pellet collection

- ghost movement

- scoring

#### Concepts demonstrated:

- pathfinding

- AI movement

- tile-based worlds

## Why ECS?
```
Entity Component Systems are widely used in modern game engines because they:

- separate data from behaviour

- improve code modularity

- allow flexible composition of game objects

- scale well for complex games

This repository implements a minimal ECS engine to demonstrate these concepts clearly.
```

## Running a Game

#### Clone the repository:

- git clone https://github.com/YOUR_USERNAME/pygame_arcade_games.git

#### Navigate into the project:

- cd pygame_arcade_games

#### Create and activate a virtual environment:

- python3 -m venv venv
- source venv/bin/activate

#### Install dependencies:

- pip install -r requirements.txt

#### Run a game:

- Snake: ````python -m snake.main````
- Tetris: ````python -m tetris.main````
- Space Invaders: ````python -m space_invaders.main````

#### Development Setup

Install development tools:

- pip install -r requirements-dev.txt

Run the formatter:

- black .

Run the linter:

- flake8 .

Run pre-commit checks:

- pre-commit run --all-files


## Future Improvements
```
Potential future enhancements include:

- Sound effects

- Sprite graphics

- Score persistence

- Leaderboards

- Particle effects
```


## Learning Objectives
```
This project is designed to improve understanding of:

- Python architecture

- Game development patterns

- Entity Component Systems

- Code modularity

- System design
```