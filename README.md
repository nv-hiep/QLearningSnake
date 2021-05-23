# SnakeQlearning
# Current Version 1.0
## Licensed under MIT license - Please feel free to modify/edit/change

Play Snake game using Reinforcement Learing (Q-learning)

## Dependencies
Code is written in python 3.<br>
1. numpy
2. pygame
3. Python3.6+

## Usage:
1. The main file is `qlearning_snake.py`

2. Q-learning algorithm in `helper\qlearner.py`

3. Other tools in `helper\tools.py`

4. A json file (`qvalues.json`) will be generated in `data\`

## To Run
- Run command:
>>> python3 qlearning_snake.py

This will create a json file <i>qvalues.json</i> in `data\`.

- You may wish to change a constant called FRAMESPEED to speed up training and play more games faster.
