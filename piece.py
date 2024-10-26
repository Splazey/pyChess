# declaration of a universal piece class
import pygame


# TODO: calibrate them to have the coordinates be accurate for all tiles
X_MULTIPLIER = 100
Y_MULTIPLIER = 100
OFFSET = 0


class Piece:

    def __init__(self, screen):
        self.selected = False
        self.screen = screen
        self.p = "white\pawn.png"  # TODO: change later, it is always white pawn for testing purposes
        self.img = pygame.image.load(self.p).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (100, 100))  # Load and scale image once
        self.rect = self.img.get_rect()  # Get rect for positioning
        self.x = 0
        self.y = 0

    def render(self):
        # Only blit the image, no need to reload it
        self.screen.blit(self.img, self.rect)

    def validate(self):
        pass

    def goto(self, c):
        if not self.validate:
            pass
        x = c[0]
        y = int(c[1])

        # Calculate the new position based on chessboard coordinates
        self.x = ((ord(x) - 96) * X_MULTIPLIER) + OFFSET
        self.y = ((9 - y) * X_MULTIPLIER) + OFFSET

        # Update rect position
        self.rect.center = (self.x, self.y)

        print(f"test piece is now in: {self.x, self.y}")

    def getHitbox(self): # a replacement of checkClicked in the older python chess, the collidepoint() is later checked in the main program
        return self.rect
    
    def toggleSelected(self):

        if self.selected:
            # TODO: let the piece go to its new position
            # TODO: set selected to false, since the player has already made the move
            pass
        else:
            pass


    
