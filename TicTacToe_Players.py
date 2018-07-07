import numpy as np


class AllPlayers(object):                                         #Parent class for all players
    def __init__(self, mark):
        self.mark = mark
        
class Hooman(AllPlayers):                                         #Hooman class for User
    pass

class Computer(AllPlayers):                                       #Computer Parent class for 'dumb' Bot and 'learning' Bot
    pass

class StartBot(Computer):                                   #'Dumb' Bot that makes random move for 'learning' Bot
    @staticmethod
    def getMove(board):                                    #'Dumb' Bot's getMove method
                empty=board.emptyBoxes()
                if empty:  
                    return empty[np.random.choice(len(empty))]    # Generates random move based on empty boxes

class Bot(Computer):                                        #Bot class for QPlayer
    def __init__(self, mark, Q={}, epsilon=0.2):
        super(Bot, self).__init__(mark=mark)
        self.Q = Q
        self.epsilon = epsilon

    def getMove(self, board):                               # QPlayer's getMove method based on QTable or a random move for exploration
        if np.random.uniform() < self.epsilon:              # Bot makes a move depending on epsilon & Q
            return StartBot.getMove(board)
        else:
            encodedState = Bot.encodeBoardState(board, self.mark, self.Q)
            QValue = self.Q[encodedState]
            if self.mark == "X":
                return Bot.random_minmax(QValue, max)
            elif self.mark == "O":
                return Bot.random_minmax(QValue, min)
    
    @staticmethod
    def random_minmax(QValue, min_or_max):       # Determines either the min or max of the QValue Table, could be random
        possibleMoves = min_or_max(list(QValue.values()))
        if list(QValue.values()).count(possibleMoves) > 1:      # If there is more than one move corresponding to the maximum Q-value, choose one at random
            bestPossibleMoves = [move for move in list(QValue.keys()) if QValue[move] == possibleMoves]
            move = bestPossibleMoves[np.random.choice(len(bestPossibleMoves))]
        else:
            move = min_or_max(QValue, key=QValue.get)
        return move

    @staticmethod
    def encodeBoardState(board, mark, Q):     # encode Board State and add to table if not already present
        initialQ = 1.0                      # Initially not a good value for QTable so that learning can be done by choosing random moves
        encodedState = board.encodeState(mark)
        if Q.get(encodedState) is None:
            Q[encodedState] = {move: initialQ for move in board.emptyBoxes()}    
        return encodedState

