import pygame

OUTLINE_WIDTH = 3
OFFSET = 0

class Square:


    def __init__(self, x, y, screen):


        self.screen = screen
        self.size = 45
        

        self.surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (255, 0, 0), (0,0, self.size * 2, self.size * 2), OUTLINE_WIDTH)

        self.x = x
        self.y = y


    def render(self):
        self.screen.blit(self.surface, (self.x - self.size - OFFSET, self.y - self.size + OFFSET))