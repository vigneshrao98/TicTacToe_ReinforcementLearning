import numpy as np
import tkinter as tk
from TicTacToe_Board import *
from TicTacToe_Players import Bot,Hooman,Computer


class Game:
    def __init__(self, root, HoomanorBot, Bot, doQLearn=None, Q={}, alpha=0.3, gamma=0.9,training=None):
        frame = tk.Frame()
        frame.grid()
        self.master = root
        self.HoomanorBot = HoomanorBot
        self.Bot = Bot
        self.firstPlayer = HoomanorBot
        self.secndPlayer = Bot
        self.board = Board()
        self.training=training
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(frame, height=2, width=4, text=" ", command=lambda i=i, j=j: self.bestMove(self.buttons[i][j]))
                self.buttons[i][j].grid(row=i, column=j, ipadx=10, ipady=10)
        self.playAgain = tk.Button(text="Play Again", command=self.restart)
        self.playAgain.grid(row=0,column=4,padx=10, pady=10)

        self.doQLearn = doQLearn
        if self.doQLearn:
            self.Q = Q
            self.alpha = alpha                                                      # Learn rate
            self.gamma = gamma                                                      # Discount factor
            self.defineQTable()

    @property
    def doQLearn(self):
        if self.performQLearn is not None:
            return self.performQLearn
        if isinstance(self.HoomanorBot, Bot) or isinstance(self.Bot, Bot):
            return True

    @doQLearn.setter
    def doQLearn(self, performQLearn):                                                   #QLearning to be done if true
        self.performQLearn = performQLearn

    def defineQTable(self):                                                              # QTable is given to players
        if isinstance(self.HoomanorBot, Bot):
            self.HoomanorBot.Q = self.Q
        if isinstance(self.Bot, Bot):
            self.Bot.Q = self.Q

    def bestMove(self, button):
        if self.board.gameOver():
            pass                                                                    # Board will be reset
        else:            
            bot_local = self.secndPlayer
            if self.empty(button):
                hooman_move = self.getMove(button)
                self.movePlayed(hooman_move)
                if not self.board.gameOver():                                       # Bot makes a move based on Q & epsilon
                    bot_move = bot_local.getMove(self.board)
                    self.movePlayed(bot_move)

    def empty(self, button):
        return button["text"] == " "

    def getMove(self, button):                                                     # Used for getting Hoomans move, QPlayer also has a getMove method
        info = button.grid_info()                                                   # Move coordinates from grid
        move = (int(info["row"]), int(info["column"]))                              
        return move

    def movePlayed(self, move):
        if self.doQLearn:                                                           # *Important* If learning is being done i.e doQLearn=true, send move to learn_Q method
            self.learn_Q(move)
        i, j = move                                                                 # Coordinates of move
        self.buttons[i][j].configure(text=self.firstPlayer.mark)                    # Placing Mark
        self.board.saveMoveToGrid(move, self.firstPlayer.mark)           # Update 
        #Check if game's gameOver
        if self.board.gameOver():  
            self.gameResult()                              # Output outcome if gameOver       
        else:
            self.nextTurn()                                     # Else switch turns

    def gameResult(self):
        if not self.training:
            if self.board.won() is None:
                print("Draw!")
            else:
                print(("Game Over. Mark {mark} won the game!".format(mark=self.firstPlayer.mark)))
        else:
            pass

    def restart(self):
        if not self.training:
            print("Play Again")
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=" ")
        self.board = Board(grid=np.ones((3,3))*np.nan)
        self.firstPlayer = self.HoomanorBot
        self.secndPlayer = self.Bot
        self.play()

    def nextTurn(self):
        if self.firstPlayer == self.HoomanorBot:
            self.firstPlayer = self.Bot
            self.secndPlayer = self.HoomanorBot
        else:
            self.firstPlayer = self.HoomanorBot
            self.secndPlayer = self.Bot

    def play(self):
        if isinstance(self.HoomanorBot, Computer) and isinstance(self.Bot, Hooman):
            self.movePlayed(HoomanorBot.getMove(self.board))
        elif isinstance(self.HoomanorBot, Computer) and isinstance(self.Bot, Computer):
            while not self.board.gameOver():        
                self.movePlayed(self.firstPlayer.getMove(self.board))  

    def learn_Q(self, move):                                                            #Learning method
        encodedState = Bot.encodeBoardState(self.board, self.firstPlayer.mark, self.Q)  #EncodedState is current state of board in numerics
        nextBoard = self.board.getUpdatedBoard(move, self.firstPlayer.mark)             #Board after move is played
        nextEncodedState = Bot.encodeBoardState(nextBoard, self.secndPlayer.mark, self.Q)
        if nextBoard.gameOver():
            reward = nextBoard.reward()                                                 #Game Over -> reward recieved 
        else:
            nextStateQ = self.Q[nextEncodedState]                                       #Get discounted rewards based on future moves
            if self.firstPlayer.mark == "X":
                reward = nextBoard.reward() + (self.gamma * min(nextStateQ.values()))   #Gamma -> discount factor  
            elif self.firstPlayer.mark == "O":
                reward = nextBoard.reward() + (self.gamma * max(nextStateQ.values()))     
        self.Q[encodedState][move] += self.alpha * (reward - self.Q[encodedState][move])#Update Q




