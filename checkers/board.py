import pygame
from .constants import ROWS, COLS, SQUARE_SIZE, PLAYER_1_COLOR, PLAYER_2_COLOR, VALID_SQUARES_COLOR, INVALID_SQUARES_COLOR
from .piece import Piece

class Board():
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.color_to_player_map = {
            PLAYER_1_COLOR: 0, 
            PLAYER_2_COLOR: 1,
            }
        self.number_pieces_player_1_2 = [12, 12]
        self.number_kings_player_1_2 = [0, 0]
        self.number_pieces_player_1 = self.number_pieces_player_2 = 12
        self.number_kings_player_1 = self.number_kings_player_2 = 0
        self.create_board()

    def draw_squares(self, window):
        window.fill(VALID_SQUARES_COLOR)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, INVALID_SQUARES_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 != row % 2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, PLAYER_2_COLOR))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, PLAYER_1_COLOR))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                field_content = self.board[row][col]
                if field_content != 0:
                    field_content.draw(window)

    def move_piece_to(self, piece, row, col):
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], self.board[row][col]
        piece.move_to(row, col)

        # no further checks needed, because of direction limitations
        if (row == 0 or row == ROWS) and not piece.is_king():
            piece.make_king()
            self.number_kings_player_1_2[self.color_to_player_map[piece.color]] += 1
            if piece.color == PLAYER_1_COLOR:
                self.number_kings_player_1 += 1
            else:
                self.number_kings_player_2 += 1
            
    def get_piece(self, row, col):
        return self.board[row][col]

    def capture_piece(self, piece):
        owner_index = self.color_to_player_map[piece.color]
        self.number_pieces_player_1_2[owner_index] -= 1
        if piece.is_king():
            self.number_kings_player_1_2[owner_index] -= 1
        self.board[piece.row][piece.col] = 0


    def can_jump_from_to(self, piece, old_row, old_col, new_row, new_col, step_size) -> bool:
        '''evaluates to True if boundaries are right and if current piece between start/end location is of different color'''
        if not (piece.is_king() or new_row == old_row + piece.direction * step_size):
            # invalid direction
            return False
        if not (0 <= new_row < ROWS and 0 <= new_col < COLS):
            # outside of board
            return False
        new_loc = self.get_piece(new_row, new_col)
        if new_loc != 0:
            # jump location not empty
            return False
        # all base obstacles have been overcome
        if step_size == 2:
            middle_row = (old_row + new_row) // 2
            middle_col = (old_col + new_col) // 2
            middle_piece = self.get_piece(middle_row, middle_col)
            if middle_piece == 0 or middle_piece.color == piece.color:
                return False
        
        return True


    def _get_valid_moves(self, piece, row, col, jump_path, step_size):
        ''' this method takes in a row and col of where the piece is currently during the jump. It also takes a jump_path so a king
        does not jump back to where it came from and to prevent jumping over the same piece twice.
        Finally a step_size is provided: if it's 1 only short jumps are considered, if 2 then jump chains are considered
        '''
        # this gets super complicated for kings, as they can move forward and backward, so in theory a ring move would be possible.
        # also, the same target location could be reached by either jumping over 1 piece or 3 pieces (in a C shape). Maybe we should then just
        # automatically decide for the longer route? The same could be true for jumping over 2 pieces, even without a king.
        # a ring move would need special caretaking: we would need to identify which pieces have already been jumped over.
        # we need to decide for the rules here.... => only in one direction possible.
        up, down, left, right = [x + y * step_size for x in [row, col] for y in [-1, +1]]
        moves = {}

        for new_col in [left, right]:
            for new_row in [up, down]:
                if not self.can_jump_from_to(piece, row, col, new_row, new_col, step_size):
                    continue
                
                if step_size == 1:
                    moves[new_row, new_col] = []
                else:
                    middle_row = (new_row + row) // 2
                    middle_col = (new_col + col) // 2
                    if (middle_row, middle_col) in jump_path:
                        continue
                    new_jump_path = jump_path.copy() #.append((middle_row, middle_col))
                    new_jump_path.append((middle_row, middle_col))
                    print(f"jump_path: {jump_path}, new jump path: {new_jump_path}")
                    moves[(new_row, new_col)] = new_jump_path
                    # recursive call
                    moves.update(self._get_valid_moves(piece, new_row, new_col, new_jump_path, step_size))
        return moves


    def get_valid_moves(self, piece):
        '''
        returns a dictionary with locations as keys and lists of pieces as values.
        '''
        moves = {}  # dictionary with valid final locations as keys and the values are the pieces that got jumped
        moves.update(self._get_valid_moves(piece, piece.row, piece.col, [], 1))
        moves.update(self._get_valid_moves(piece, piece.row, piece.col, [], 2))

        return moves

