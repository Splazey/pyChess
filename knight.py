
import pygame
from piece import Piece

BLACK = "black\knight.png"
WHITE = "white\knight.png"


class Knight(Piece):


    def __init__(self, screen, color):
        super().__init__(screen)

        if color == 'b':
            self.p = BLACK
        else:
            self.p = WHITE
    
        self.img = pygame.image.load(self.p).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (100, 100))

    def validate(self):
        pass