# 2D-Shooting-Game

This project is a simple 2D shooting game developed using Pygame. It features a player-controlled spaceship that can move in four directions and shoot enemies that appear on the screen. The game includes special power-ups like auto-fire and multi-direction shooting to enhance the gameplay experience.

## Features

- **Player Movement**: The player can move left, right, up, and down using the arrow keys.
- **Shooting Mechanics**: Press the space bar to shoot bullets. The game supports single-shot and continuous auto-fire modes, which can be activated by collecting power-ups.
- **Enemies**: Various types of enemies challenge the player with different behaviors and attack patterns.
- **Power-Ups**: Enhance the player's shooting capabilities temporarily. Power-ups include auto-fire and multi-direction shooting.
- **Score System**: Points are awarded for each enemy destroyed. The score is displayed on the screen.
- **Game Over Conditions**: The game ends when the player loses all lives.

## Technologies Used

- **Python 3.8**: Main programming language.
- **Pygame**: Python library for writing video games.

## Setup

To run this game, you need to have Python and Pygame installed on your system.

1. **Install Python**

   Download and install Python from [python.org](https://www.python.org/downloads/).

2. **Install Pygame**

   After installing Python, install Pygame by running this command in your terminal:

   ```bash
   pip install pygame

3.  **Download the Game**
   Clone or download this repository to your local machine.

5. **Run the Game**
   Navigate to the game directory in your terminal and run the following command:
   python main.py

## File Structure
- main.py: The entry point of the game, which initializes the game and contains the main game loop.
- game_entities.py: Defines the game entities like Player, Enemy, Bullet, and PowerUp.
- game_functions.py: Contains functions for game initialization, event handling, and game state updates.
