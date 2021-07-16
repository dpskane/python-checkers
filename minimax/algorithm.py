from copy import deepcopy
import pygame
from ..checkers.constants import PLAYER_1_COLOR, PLAYER_2_COLOR

def minimax(board_state, depth, maximizing, game):
    '''
    board_state: a board state
    depth: the current depth of the minimax algorithm
    maximizing: a boolean value to indicate whether the algorithm should maximize or minimize atm
    game: the whole game
    '''
    if depth == 0 or board_state.winner != None:
        return board_state.evaluate(), board_state
    
    if maximizing:
        maxEval  = float('-inf')
        best_move = None
        for move in get_all_moves(board_state, PLAYER_1_COLOR, game)
    else:
        