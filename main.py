import pygame
import board
from highlighter import Highlighter


SCREEN_WIDTH, SCREEN_HEIGHT = 900,900
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((0,0,0)) # fill the screen with black color
pygame.display.set_caption("PyChess Project") # Window title


b = board.Board(screen)
b.setFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR") # FEN code for the chess board position
turn = True

# main game loop
running = True

while running:
    b.blitBoard() # render the board itself

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # Get the x and y coordinates of the click
            if b.movePiece(x, y, turn):
                turn = not turn # if a piece has been moved (movePiece() returns a True status), change the turns

    b.renderHighlights() # render the highlights made by the board

    b.renderPieces() # render the pieces stored in the board

    pygame.display.update()  # Update the display