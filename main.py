import pygame
import board
from highlighter import Highlighter


SCREEN_WIDTH, SCREEN_HEIGHT = 900,900
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((0,0,0)) # fill the screen with black color
pygame.display.set_caption("PyChess")


# TODO the turn system will be implemented in main


#variables go below:


# TODO make a variable that stores the piece that is being selected
b = board.Board(screen)
b.setFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
turn = True
# test = Highlighter(screen)
# test.circleHighlight(["b2"])

# ----------------- 

# main game loop

running = True

while running:
    b.blitBoard()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # Get the x and y coordinates of the click
            print(f"You clicked on {b.getTile(x, y)}")
            # print(f"x={x}, y={y}")
            if b.movePiece(x, y, turn):
                turn = not turn
            # test.goto(b.getTile(x, y))
            # let the board object use its getTile() method and find what piece is being clicked on 

    # test.renderElements()

    b.renderHighlights() # render the highlights made by the board

    b.renderPieces() # render the pieces stored in the board

    pygame.display.update()  # Update the display