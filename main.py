import pygame
from checkers.constants import WIDTH, HEIGHT
from checkers.board import Board

board = Board()
FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        # event.get() returns all events that happened since the last tick
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        board.draw_squares(WINDOW)
        pygame.display.update()
        
    pygame.quit()

main()


