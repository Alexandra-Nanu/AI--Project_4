# Pacman Multi-Agent Systems

This project introduces multi-agent decision-making techniques to model interactions between Pacman and ghosts, balancing strategy and survival.

## License

This project is for educational purposes and follows the **Berkeley AI Pacman Project** framework.  
Please note that the project has been solved in teams of 2:

- Alexandra Nanu's work is marked under `@Author: Alexandra Nanu`
- Paula Moldovan's work is marked under `"""Paula Moldovan"""`

## Overview

This project extends basic search strategies to multi-agent environments, applying **game theory** techniques like **Minimax, Alpha-Beta Pruning, and Expectimax** to optimize Pacman's gameplay.

### Implemented Algorithms
- Reflex Agent: A basic agent that reacts to food and ghosts
- Minimax Search: Computes an optimal strategy against adversarial ghosts
- Alpha-Beta Pruning: Optimizes Minimax by pruning unnecessary branches
- Expectimax Search: Handles probabilistic ghost behavior
- Improved Evaluation Function: Enhances Pacman’s decision-making
- This project builds on basic search techniques, introducing multi-goal search problems and heuristic optimizations to enhance efficiency. Pacman must now navigate mazes while solving more complex constraints.

## How to Run the Search Agents

Test different search strategies by running:
- **Reflex Agent:**
  `python pacman.py -p ReflexAgent -l mediumClassic -k 1`
- **Minimax Agent:***
  `python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4`
- **Alpha-Beta Pruning Agent:**
  `python pacman.py -p AlphaBetaAgent -l minimaxClassic -a depth=4`
- **Expectimax Agent:**
  `python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3`
- **Improved Evaluation Agent:**
  `python pacman.py -p BetterEvaluationAgent -l smallClassic`
- Use `-h ` for a list of available options:
  `python pacman.py -h`
- Run the autograder to test the given implementation:
  `python autograder.py`

## File Structure
- `multiAgents.py`– Implements multi-agent decision-making algorithms
- `pacman.py` – Main game engine
- `util.py` – Helper functions for data structures
