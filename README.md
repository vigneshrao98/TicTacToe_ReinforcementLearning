# TicTacToe_ReinforcementLearning

A TicTacToe game written in python with a reinforcement learning bot

# HOW TO

1. Install Python 2.7.X or 3.5.x from [here](https://www.python.org/download/releases/)

2. Clone this repository: `git clone https://github.com/vigneshrao98/TicTacToe_ReinforcementLearning.git` or click `Download ZIP` in right panel and extract it.

3. In command line enter *pip i nstall numpy* to install numpy which is a library used in the scripts.

4. Navigate to the right folder in command line and enter  *python Play_against_bot.py* to play against a bot who has learnt from playing against itself using reinforcement learning!
   
5. To train bot enter *python Bot_training.py* ,this will make a the bot play and learn against itself for 150,000 games!
 
# FILES
 - TicTacToe_Players.py : Implements classes for different players i.e. the user and the bot.
 - TicTacToe_Board.py : Implements classes for the game grid.
 - TicTacToe_Game.py : Implements the environment for a TicTakToe game.
 - Play_against_bot.py : Script to play a game against the bot.
 - Bot_training.py : Script to train the bot by playing against itself, and dumps data to disk using pickle.
 - dataQTable_150000_games : QTable(Experience) of the bot learning from 150,000 games!
 
# Training Parameters
 - Exploration factor for playing against user : 0  
   This is to ensure it follows the optimal policy and tries to win the game against user.
 - Exploration factor while training : 0.9
   To ensure it explores new moves while trying to learn to discover optimal strategies to win.
 - Learning parameter Alpha : 0.25
 - Decay factor Gamma : 0.95
 



