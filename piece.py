# declaration of a universal piece class
import pygame


# TODO: calibrate them to have the coordinates be accurate for all tiles
X_MULTIPLIER = 100
Y_MULTIPLIER = 100
OFFSET = 100


class Piece:

    def __init__(self, screen, x, y):
        self.selected = False
        self.screen = screen
        self.p = "white\pawn.png"  # TODO: change later, it is always white pawn for testing purposes
        self.img = pygame.image.load(self.p).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (100, 100))  # Load and scale image once
        self.rect = self.img.get_rect()  # Get rect for positioning


        self.x = (x* X_MULTIPLIER) + OFFSET
        self.y = (y * Y_MULTIPLIER) + OFFSET

        self.rect.center = (self.x, self.y)

    def render(self):
        # Only blit the image, no need to reload it
        self.screen.blit(self.img, self.rect)

    def checkLegal(self, x,y,board): # for polymorphism, this function is different in every child class, since each piece has different rules to be moved
        pass

    def destroyPiece(self):
        self


    def goto(self, c, board):
        

        x = c[0]
        y = int(c[1])


        cx = (self.x - OFFSET) // 100
        cy = (self.y - OFFSET) // 100
        print(f"GOTO: {cx},{cy}")

        
        if c not in self.checkLegal(cx, cy, board):
            print("Illegal Move Detected")
            return False


        # Calculate the new position based on the board array coordinates
        self.x = ((ord(x) - 96) * X_MULTIPLIER)
        self.y = ((9 - y) * X_MULTIPLIER)

        # Update rect position
        self.rect.center = (self.x, self.y)

        return True