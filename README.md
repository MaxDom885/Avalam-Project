# Avalam Project

This project implements the Avalam game, a strategy game where two players compete on a board by moving and stacking towers of tokens of different heights. The project also includes an implementation of the game of tic-tac-toe using the MiniMax algorithm with a graphical interface.

## Project Structure

The project is organized into several files:

- `avalam.py`: Contains the logic of the Avalam game, including the board representation and the rules of the game.
- `alphabeta_player.py`: Implements an agent using the Alpha-Beta algorithm to play Avalam.
- `player.py`: Contains the implementation of your custom agent for the contest.
- `random_player.py` : Implements a random player to test the game.
- `game.py` : Manages the Avalam game flow, including player management and user interface.
- `gui.py` : Provides a graphical interface for the Tic-Tac-Toe game.
- `tictactoe.py` : Contains the logic for the Tic-Tac-Toe game.
- `minimax_player.py` : Implements an agent that uses the MiniMax algorithm to play Tic-Tac-Toe.
- `game_runner.py` : Contains the logic to run the Tic-Tac-Toe game and allow players to play against the MiniMax agent.

## Authors

- ATTOH James
- BIAOU Marius
- HOUESSOU Kenny
- YACOUBOU Masmoud

## Prerequisites

- Python 3.9 or higher
- `tkinter` library for the GUI

## Installation

1. **Install Python 3.9 or higher**: Make sure you have Python 3.9 or later installed on your machine. You can check your Python version with the following command:
```sh
python --version
```

2. **Install dependencies**: You will need some Python libraries. You can install them via `pip` :
```sh
pip install xmlrpcserver
```

## Run the Avalam Game

### Run the Game with Two Human Players

```sh
python game.py human human
```
### Run the Game with One Human Player and One Random Player
In a terminal :
```sh
python random_player.py -p 8000
```
In another terminal :
```sh
python game.py human http://localhost:8000
```
### Run the Game with One Human Player and One AI Agent (Alpha-Beta)
In a terminal :
```sh
python alphabeta_player.py -p 8000
```
### In another terminal :
```sh
python game.py human http://localhost:8000
```
### Running the Game with a Human Player and Your Custom Agent
In a terminal:
```sh
python player.py -p 8000
```
### In another terminal:
```sh
python game.py human http://localhost:8000
```
### Running the Tic-Tac-Toe Game with the GUI
To use the GUI, make sure you have the Tk bindings for Python installed. On Debian-based systems, you can install the python3-tk package:
```sh
sudo apt-get install python3-tk
```
Then, run the game with the GUI:
```sh
python gui.py
```
### Advanced Commands
Recording a Game
```sh
python game.py human human -w trace.pkl
```
### Replaying a Recorded Game
```sh
python game.py -r trace.pkl
```
### Setting a Credit Time per Player
```sh
python game.py human human -t 60
```
### Inverting the Initial Board
```sh
python game.py human human --invert
```
### Setting the Maximum Tower Height
```sh
python game.py human human --tower-height 6
```
### Load a Custom Initial Board
```sh
python game.py human human --board custom_board.csv
```
### Disable GUI
```sh
python game.py human human --no-gui
```
### Run the Game in Headless Mode (without User Interface)
```sh
python game.py human human --headless
```
### Enable Verbose Mode
```sh
python game.py human human -v
```
