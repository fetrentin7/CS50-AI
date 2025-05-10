"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    player_x = 0
    player_y = 0
    for row in board:
        for cell in row:

            if cell == 'X':
                player_x += 1
            elif cell == 'O':
                player_y += 1

    if player_x <= player_y:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()

    for row in range(3):
        for column in range(3):
            if board[row][column] is EMPTY:
                moves.add((row, column))

    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)

    if action not in actions(board):
        raise Exception("Empty")

    i, j = action
    new_board[i][j] = player(board)
    return new_board

def checkColumn(board):

    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] != EMPTY:
            return board[0][column]

    return None

def checkLine(board):

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != EMPTY:
            return board[row][1]

    return None

def checkDiagonal(board):

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
       return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
       return board[0][2]

    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    return checkLine(board) or checkColumn(board) or checkDiagonal(board)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)

    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


def minimax(board):
    if terminal(board):
        return None


    current = player(board)

    if current == X:
        best_score = -math.inf
        best_move = None
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_move = action
        return best_move

    else:
        best_score = math.inf
        best_move = None
        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_move = action

        return best_move


def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf
    for a in actions(board):
        v = min(v, max_value(result(board, a)))
    return v

def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for a in actions(board):
        v = max(v, min_value(result(board, a)))
    return v
