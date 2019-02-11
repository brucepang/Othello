from engines import Engine
from copy import deepcopy

class StudentEngine(Engine):
    """ Game engine that you should you as skeleton code for your 
    implementation. """
    search_depth = 2
    alpha_beta = False

    def get_move(self, board, color, dupSet, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Wrapper function that chooses either vanilla minimax or 
        alpha-beta. """
        f = self.get_ab_minimax_move if self.alpha_beta else self.get_minimax_move
        self.exp = Experiment()
        self.exp.prevStates = dupSet
        return f(board, color, move_num, time_remaining, time_opponent)

    def get_minimax_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Skeleton code from greedy.py to get you started. """
        self.color = color
        _,move = self.minimax_cost(board, self.search_depth, True, color)
        return move

    def get_ab_minimax_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Skeleton code from greedy.py to get you started. """
        alpha, beta = -float("inf"), float("inf")
        self.color = color
        _,move = self.minimax_ab_cost(board, self.search_depth, alpha, beta, True, color)
        return move

    def _get_cost(self, board, color, move):
        """ Return the difference in number of pieces after the given move 
        is executed. """
        
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, color)

        # Count the # of pieces of each color on the board
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))

        # Return the difference in number of pieces
        return num_pieces_me - num_pieces_op

    def minimax_cost(self,board,depth,maximizingPlayer,color):
        moves = board.get_legal_moves(color)

        # Experiment Part
        if self.exp.containState(board):
            self.exp.addDuplicate()
        else:
            self.exp.saveState(board)

        if depth == 0 or len(moves) == 0:
            return self.heuristic(board),None

        # Experiment Part
        self.exp.addBranch(len(moves))

        if maximizingPlayer:
            maxEval = -float("inf")
            res_move = None
            for move in moves:
                
                newboard = deepcopy(board)
                newboard.execute_move(move,color)

                # Experiment Part
                self.exp.addNode()
               
                evalulation,_ = self.minimax_cost(newboard,depth-1,not maximizingPlayer,color*-1)
                # maxEval = max(maxEval,evalulation)
                if evalulation > maxEval:
                    maxEval,res_move = evalulation,move
            return maxEval,res_move
        else:
            minEval = float("inf")
            res_move = None
            for move in moves:

                newboard = deepcopy(board)
                newboard.execute_move(move,color)

                # Experiment Part
                self.exp.addNode()

                evalulation,_ = self.minimax_cost(newboard,depth-1,not maximizingPlayer,color*-1)
                # minEval = min(minEval,evalulation)
                if evalulation < minEval:
                    minEval = evalulation
                    res_move = move
            return minEval,res_move


    def minimax_ab_cost(self,board,depth,alpha,beta,maximizingPlayer,color):
        moves = board.get_legal_moves(color)

        # Experiment Part
        if self.exp.containState(board):
            self.exp.addDuplicate()
        else:
            self.exp.saveState(board)

        if depth == 0 or len(moves) == 0:
            return self.heuristic(board), None

        # Experiment Part
        self.exp.addBranch(len(moves))

        if maximizingPlayer:
            maxEval = -float("inf")
            res_move = None
            for move in moves:

                newboard = deepcopy(board)
                newboard.execute_move(move,color)

                # Experiment Part
                self.exp.addNode()
                
                evalulation,_ = self.minimax_ab_cost(newboard,depth-1,alpha,beta,not maximizingPlayer,color*-1)
                if evalulation > maxEval:
                    maxEval,res_move = evalulation,move
                alpha = max(alpha,evalulation)
                if beta <= alpha:
                    break
            return maxEval,res_move
        else:
            minEval = float("inf")
            res_move = None
            for move in moves:

                
                newboard = deepcopy(board)
                newboard.execute_move(move,color)

                # Experiment Part
                self.exp.addNode()

                evalulation,_ = self.minimax_ab_cost(newboard,depth-1,alpha,beta,not maximizingPlayer,color*-1)
                if evalulation < minEval:
                    minEval,res_move = evalulation,move
                beta = min(beta, evalulation)
                if beta <= alpha:
                    break
            return minEval,res_move


    def heuristic(self,board):
        # number of black - number of white
        return 15*self.coin_parity(board)+\
               30*self.mobility(board)+\
               600*self.corner_capture(board)


    def coin_parity(self,board):
        num_pieces_op = board.count(self.color*-1)
        num_pieces_me = board.count(self.color)
        return 100*(num_pieces_me-num_pieces_op)/(num_pieces_me+num_pieces_op)

    def mobility(self,board):
        legal_move_me = len(board.get_legal_moves(self.color))
        legal_move_op = len(board.get_legal_moves(self.color*-1))
        if legal_move_op + legal_move_me == 0:
            return 0
        else:
            return 100*(legal_move_me-legal_move_op)/(legal_move_me+legal_move_op)

    def corner_capture(self,board):
        corners = [(0,0),(0,7),(7,0),(7,7)]
        corner_me = 0
        corner_op = 0
        for x,y in corners:
            if board[x][y] == self.color:
                corner_me+=2
            elif board[x][y] == self.color*-1:
                corner_op+=2
            if (x,y) in board.get_legal_moves(self.color):
                corner_me+=1
            if (x,y) in board.get_legal_moves(self.color*-1):
                corner_op+=1
        if corner_me + corner_op == 0:
            return 0
        else:
            return 100*(corner_me-corner_op)/(corner_me+corner_op)

class Experiment():
    def __init__(self):
        self.num_nodes = 0
        self.prevStates = set()
        self.duplicate = 0
        self.branch = []

    def addNode(self):
        self.num_nodes+=1

    def getNode(self):
        return self.num_nodes

    def saveState(self,board):
        serialized = ""
        for y in range(8):
            for x in range(8):
                serialized+=str(board[x][y])
        self.prevStates.add(serialized)

    def getStates(self):
        return self.prevStates

    def containState(self,board):
        serialized = ""
        for y in range(8):
            for x in range(8):
                serialized+=str(board[x][y])
        return serialized in self.prevStates

    def addDuplicate(self):
        self.duplicate+=1

    def getDuplicate(self):
        return self.duplicate

    def addBranch(self,num):
        self.branch.append(num)

    def getBranch(self):
        return self.branch

engine = StudentEngine
