# Pixel Rabbit Adventure

A pixel-art 2D side-scrolling action platformer where you control a heroic rabbit with a red scarf, fighting enemies and collecting carrots through three challenging levels.

## Features

- Pixel-art style 2D side-scrolling action gameplay
- Three unique levels with increasing difficulty
- Multiple enemy types:
  - Grunt: patrols platforms
  - Gunner: patrols and shoots projectiles
  - Boss: a powerful enemy in the final level
- Collectible system: collect carrots to replenish ammo
- Smooth camera following system
- Health, lives, and ammo system
- All UI and in-game text in English

## Controls

- Arrow keys or A/D: Move
- Space: Jump
- J: Shoot
- Game over returns to main menu

## Installation

1. Make sure you have Python 3.7 or higher installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

```bash
python src/main.py
```

## Game Objectives

- Defeat all enemies
- Collect carrots to replenish ammo
- Survive the boss fight
- Complete all three levels

## Project Structure

- `src/main.py`: Game entry point
- `src/game.py`: Core game logic
- `src/player.py`: Player class
- `src/enemy.py`: Enemy classes
- `src/level.py`: Level management
- `src/camera.py`: Camera system
- `src/projectile.py`: Projectile classes

## TODO

- [ ] Add sound effects and background music
- [ ] Add more animations
- [ ] Implement save system
- [ ] Add more levels
- [ ] Optimize game performance 