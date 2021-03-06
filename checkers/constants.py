import pygame

WIDTH = HEIGHT = 600
ROWS = COLS = 8
SQUARE_SIZE = WIDTH // COLS
PIECE_PADDING = 12
PIECE_OUTLINE = 2
PIECE_RADIUS = SQUARE_SIZE // 2 - PIECE_PADDING

# rgb
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

PLAYER_1_COLOR = RED        # bottom player, moves up (-1 direction)
PLAYER_2_COLOR = GREEN

HIGHLIGHT_COLOR = BLUE

VALID_SQUARES_COLOR = WHITE
INVALID_SQUARES_COLOR = BLACK

CROWN_WIDTH = (PIECE_RADIUS * 9 ) // 5
CROWN_HEIGHT = PIECE_RADIUS
CROWN_IMG = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (CROWN_WIDTH, CROWN_HEIGHT))
