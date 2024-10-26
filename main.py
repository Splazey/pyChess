import pygame
import board


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
# ----------------- 


board = pygame.image.load("board.png")
board = pygame.transform.smoothscale(board, (SCREEN_WIDTH, SCREEN_HEIGHT))

# test = Piece(screen)
# test.goto("a1")

# main game loop

running = True

while running:
    screen.blit(board, (0, 0))  # Render the board first

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # Get the x and y coordinates of the click
            print(f"You clicked on {b.getTile(x, y)}")
            print(f"x={x}, y={y}")
            # test.goto(b.getTile(x, y))
            # let the board object use its getTile() method and find what piece is being clicked on 

    b.renderPieces()
    pygame.display.update()  # Update the display