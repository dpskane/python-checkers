import pygame
from .constants import GREY, SQUARE_SIZE, PIECE_RADIUS, PIECE_OUTLINE, CROWN_IMG, PLAYER_1_COLOR, PLAYER_2_COLOR

class Piece:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self._king = False
        self.direction = 1 if self.color == PLAYER_2_COLOR else -1

        self.x = 0
        self.y = 0
        self.calculate_position()

    def move_to(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()

    def calculate_position(self):
        self.x = int((self.col + 0.5) * SQUARE_SIZE)
        self.y = int((self.row + 0.5) * SQUARE_SIZE)

    def make_king(self):
        self._king = True

    def is_king(self) -> bool:
        return self._king

    def draw(self, window):
        pygame.draw.circle(window, GREY, (self.x, self.y), PIECE_RADIUS + PIECE_OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), PIECE_RADIUS)
        if self._king:
            window.blit(CROWN_IMG, (self.x - CROWN_IMG.get_width() // 2, self.y - CROWN_IMG.get_height() // 2))

    def __repr__(self):
        return str(self.color)
