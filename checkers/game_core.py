import pygame
from .constants import PLAYER_1_COLOR, PLAYER_2_COLOR, HIGHLIGHT_COLOR, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, window):
        self.window = window
        self._init()

    def _init(self):
        self.selected_piece = None
        self.turn = PLAYER_1_COLOR
        self.valid_moves_of_selected_piece = {}
        self.board = Board()

    def reset(self):
        self._init()

    def winner(self):
        return self.board.winner

    def update(self):
        self.board.draw(self.window)
        self._draw_valid_moves(self.valid_moves_of_selected_piece)
        pygame.display.update()

    def _change_turn(self):
        if self.turn == PLAYER_2_COLOR:
            self.turn = PLAYER_1_COLOR
        else:
            self.turn = PLAYER_2_COLOR
        self.update()
        if not self.board.has_valid_moves(self.turn):
            self.board.winner = 1 - self.board.color_to_player_map[self.turn]

    def _draw_valid_moves(self, moves):
        for move in moves:
            row_pos, col_pos = [int((x + 0.5) * SQUARE_SIZE) for x in move]
            pygame.draw.circle(self.window, HIGHLIGHT_COLOR, (col_pos, row_pos), SQUARE_SIZE // 4)        

    def _move(self, row, col) -> bool:
        # move the piece that is selected
        target = self.board.get_piece(row, col)
        if target == 0 and (row, col) in self.valid_moves_of_selected_piece:
            self.board.move_piece_to(self.selected_piece, row, col)
            for enemy_piece_loc in self.valid_moves_of_selected_piece[(row, col)]:
                row, col = enemy_piece_loc
                enemy_piece = self.board.get_piece(row, col)
                self.board.capture_piece(enemy_piece)
            self._change_turn()
            return True
        else:
            return False

    def select(self, row, col) -> bool:
        if self.selected_piece:
            # try moving the piece to the new location
            successful_move = self._move(row, col)
            if successful_move:
                self.selected_piece = None
                self.valid_moves_of_selected_piece = {}
                return False
            else:
                # if not successful, deselect the current piece. Try to select the piece in the new location instead if possible
                self.selected_piece = None
                return self.select(row, col)
        else:
            # try to select the piece under the mouse
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                # the square under the cursor has a piece of the player's color: select it
                self.selected_piece = piece
                self.valid_moves_of_selected_piece = self.board.get_valid_moves(piece)
                #print(f"location: ({row}, {col})")
                #print(f"valid moves: {self.valid_moves}")
                return True
            else:
                return False

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self._change_turn()

    
