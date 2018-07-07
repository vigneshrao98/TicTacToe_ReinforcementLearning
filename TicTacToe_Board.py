import numpy as np
import copy

#class Board for making Tic Tac Toe grid, and required grid functions

class Board:
    def __init__(self, grid=np.ones((3,3))*np.nan):
        self.grid = grid                                                                # Grid acting as memory storing 1 for X and 0 for Y

    def won(self):
        # Checking for 3 of same mark in a row,column or diags to see if any mark won

        allThree=np.concatenate(([self.grid[:,j] for j in range(3)],
                                 [self.grid[i,:] for i in range(3)],
                                 [np.array([self.grid[i,i] for i in range(3)])],
                                 [np.array([self.grid[2-i,i] for i in range(3)])]  ))   # allThree contains continuous rows,cols and diags     

        tripleMark = lambda x: any([np.array_equal(y, x) for y in allThree])            #Search for same mark in allThree 

        if tripleMark(np.ones(3)):                                                      #1->X won
            return "X"
        elif tripleMark(np.zeros(3)):                                                   #0->O won
            return "O"


    def saveMoveToGrid(self, move, mark):      
        dic = {"X": 1, "O": 0}                                                          # Save move(X->1,O->0) to memory i.e. grid
        self.grid[tuple(move)] = dic[mark]
        
    def gameOver(self):                                                                 #Game Over if draw or some player wins
        draw=not np.any(np.isnan(self.grid))
        gameWon=self.won() is not None
        return draw or gameWon

    def emptyBoxes(self):                                                               #Return remaining empty squares
        return [(i,j) for i in range(3) for j in range(3) if np.isnan(self.grid[i][j])]

    def getUpdatedBoard(self, move, mark):                                              #Returns updated board with placed mark
        newcopy = copy.deepcopy(self)
        newcopy.saveMoveToGrid(move, mark)
        return newcopy

    def encodeState(self, mark):                                                        #Encodes current board state for Q
        filled_grid = copy.deepcopy(self.grid)
        np.place(filled_grid, np.isnan(filled_grid),9)
        return "".join(map(str, (list(map(int, filled_grid.flatten()))))) + mark

    def reward(self):                               # Give reward for the QPlayer when game is over
        if self.gameOver():
            if self.won() is not None:
                if self.won() == "X":
                    return 1.0                      # +1 Reward for QPlayer as game won
                elif self.won() == "O":
                    return -1.0                     # -1 Reward for QPlayer as game lost
            else:
                return 0.5                          # 0.5 Reward for QPlayer cause game draw
        else:
            return 0.0                              # No reward till game is over