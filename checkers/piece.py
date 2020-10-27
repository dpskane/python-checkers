import pygame
from .constants import RED, WHITE, GREY, SQUARE_SIZE, PIECE_RADIUS, PIECE_OUTLINE

class Piece:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.direction = 1 if self.color == WHITE else -1

        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = (self.col + 0.5) * SQUARE_SIZE 
        self.y = (self.row + 0.5) * SQUARE_SIZE

    def make_king(self):
        self.king = True

    def draw(self, window):
        pygame.draw.circle(window, GREY, (self.x, self.y), PIECE_RADIUS + PIECE_OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), PIECE_RADIUS)

    def __repr__(self):
        return str(self.color)