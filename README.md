# 🎮 Game Hub — CS108 Project

A multi-game interactive hub built with Python and Pygame, featuring three classic board games with a shared leaderboard, match history, and player statistics.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Games](#games)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [User System](#user-system)
- [Leaderboard](#leaderboard)
- [Contributors](#contributors)

---

## Overview

Game Hub is a 2-player local game platform developed for CS108. Players log in with usernames, choose a game from the main menu, and compete head-to-head. Results are saved to a match history file, and a leaderboard tracks performance across sessions.

---

## Games

### Tic-Tac-Toe
The 10X10 grid game. Two players alternate placing their marks (cross vs. circle). First to get five in a row wins.

### Connect 4
A 2-player strategy game on a vertical grid of 7X7. Players drop colored discs into columns; the first to align four discs horizontally, vertically, or diagonally wins.

### Othello (Reversi)
A 8×8 board strategy game where players place discs to flip the opponent's pieces. The player with the most discs when the board is full wins.

---

## Features

- **Multi-game hub** — unified main menu to launch any of the three games
- **User login & registration** — players log in via the terminal before the game starts
- **Match history** — all game results are recorded to `history.csv`
- **Leaderboard** — sortable leaderboard with win/loss statistics, viewable from the terminal or in-game
- **Game statistics plots** — performance charts generated with Matplotlib
- **Custom UI** — Pygame interface with custom fonts (Cinzel), animated sprites, and themed visuals per game
- **Game-over screens** — win/loss screens with options to play again, view the leaderboard, return to menu, or quit
- **Two-player local co-op** — designed for two players on the same machine

---

## Project Structure

```
Project_for_cs108/
│
├── game.py               # Core classes: Game, Player, Board; shared UI logic
├── main.sh               # Entry point — handles user login and launches the game
├── leaderboard.sh        # Shell script to display and sort the leaderboard
│
├── games/
│   ├── tictactoe.py      # Tic-Tac-Toe game logic and rendering
│   ├── connect4.py       # Connect 4 game logic and rendering
│   ├── othello.py        # Othello game logic and rendering
│   └── __init__.py
│
├── images/               # All game assets (boards, sprites, buttons, backgrounds)
├── fonts/                # Cinzel and EB Garamond font files
│
├── games.csv             # Maps game names to their script paths
├── users.tsv             # Registered users database
├── history.csv           # Match history log
├── coords.txt            # Coordinate data (used for board layout)
└── plot.png              # Generated statistics plot
```

---

## Requirements

- Python 3.10+
- `pygame`
- `numpy`
- `matplotlib`

Install dependencies with:

```bash
pip install pygame numpy matplotlib
```

---

## How to Run

From the project root directory, run:

```bash
bash main.sh
```

This will:
1. Prompt **Player 1** to log in or register
2. Prompt **Player 2** to log in or register
3. Launch the Pygame game hub window

From the hub, click a game to start playing. After the game ends, results are saved and you can navigate back to the menu or view the leaderboard.

To view the leaderboard separately:

```bash
bash leaderboard.sh
```

---

## User System

Users are stored in `users.tsv`. When a player enters a username that doesn't exist, they are prompted to register. Usernames must be non-empty and unique.

Player data is passed to the game and tied to match history for leaderboard tracking.

---

## Leaderboard

The leaderboard tracks each player's wins and losses across all games. It can be sorted by different criteria via `leaderboard.sh`. An in-game leaderboard view is also accessible from the game-over screen.

---

## Contributors

| Branch | Focus Area |
|--------|------------|
| `main` | Core game hub and shared logic |
| `GAME_MODIFICATIONS` | Individual game improvements |
| `LEADERBOARD_MODIFICATIONS` | Leaderboard feature |
| `HISTORY_MODIFICATIONS` | Match history tracking |
| `2PGAMES_MODIFICATIONS` | Two-player game support |
| `Charwin_Updates` | UI and visual updates |
| `development` | Active development branch |