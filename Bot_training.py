from TicTacToe import Game, Bot     # Classes used for Tic Tac Toe
import pickle as pik
import numpy as np
import tkinter as tk
import copy

#Player1 -> exploring bot, Player2 -> exploring bot

episodes = 150000                                    #No. of games to be played against itself
saveToFile="dataQTable_{}_games.p".format(episodes)  #File to save QTable in

root=tk.Tk()
game = Game(root, Bot(epsilon = 0.9,mark="X"), Bot(epsilon = 0.9,mark="O"),training=True)

for episodes in range(episodes):
    game.play()
    game.restart()
    if episodes%1000==0:
        print(str(episodes)+ " episodes done!")

Q = game.Q                                    #Q to be saved to disk
pik.dump(Q, open(saveToFile, "wb"))
