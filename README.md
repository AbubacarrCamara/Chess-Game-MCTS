# Chess-Game-MCTS

Overview

This project is a command-line chess game built in Python. It fully supports standard chess rules, including castling, en passant, checkmate, and move validation. The game is designed using an object-oriented approach, making it modular and extendable for future improvements like AI-based move generation using Monte Carlo Tree Search (MCTS).

Features

Complete chess rules enforcement (legal move validation, check detection, checkmate, and stalemate handling).

Turn-based gameplay with support for two players.

Command-line interface (CLI) for making moves using algebraic notation (e.g., e2 e4).

Piece movement logic implemented for all pieces, including pawns, knights, bishops, rooks, queens, and kings.

Special moves supported:

Castling (king-side and queen-side)

En passant captures

Pawn promotion

Planned Improvements

Core Mechanics



AI & Automation



User Interface & Experience



Performance Optimization



Installation

Prerequisites

Ensure you have Python installed (version 3.7+ recommended).

Clone the Repository

git clone https://github.com/your-repo/chess-game.git
cd chess-game

Run the Game

python Chess_MCTS.py

How to Play

The game starts with White making the first move.

Enter moves using algebraic notation, e.g., e2 e4 (move piece from e2 to e4).

The board updates and switches turns automatically.

The game continues until a checkmate, stalemate, or draw condition is met.

If an invalid move is attempted, the game will prompt you to enter a valid move.

Future Plans

This chess engine will serve as the foundation for an AI-powered chess opponent using MCTS. The goal is to simulate thousands of potential games and refine AI decision-making based on probabilistic outcomes rather than hard-coded heuristics.

Contributions

Contributions are welcome! Feel free to fork the repository and submit pull requests.

License

This project is open-source and available under the MIT License.
