import numpy as np
import pickle as pik 
import tkinter as tk
import copy
from TicTacToe_Game import Game, Hooman, Bot

#Player1 -> hooman, Player2 -> trained bot
#change read file***********
readFromFile="dataQTable_150000_games.p"  #File to read QTable from

Q = pik.load(open(readFromFile,"rb"))

root=tk.Tk()
game = Game(root, Hooman(mark="X"),  Bot(mark="O", epsilon=0), Q=Q)

game.play()
root.mainloop()
