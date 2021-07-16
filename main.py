import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from checkers.game_core import Game


FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    print("game started")

    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            print("winner" + str(game.winner()))
            break

        # event.get() returns all events that happened since the last tick
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_pos(pos)
                #piece = board.get_piece(row, col)
                game.select(row, col)
                #board.move_piece_to(piece, 3, 2)

        game.update()

    pygame.quit()

main()


