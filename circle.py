import pygame


OFFSET = 2


class Circle:


    def __init__(self,x, y, screen):
        


        self.screen = screen
        self.alpha_level = 40
        self.radius = 15

        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, (0,0,0,self.alpha_level), (self.radius, self.radius), self.radius)

        # print(f"surface {self.surface}")

        self.x = x
        self.y = y



    def render(self):
        self.screen.blit(self.surface, (self.x - self.radius - OFFSET, self.y - self.radius + OFFSET))