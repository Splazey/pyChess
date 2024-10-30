import pygame
from circle import Circle


X_MULTIPLIER = 100
Y_MULTIPLIER = 100



class Highlighter:


    def __init__(self, screen):
        self.screen = screen
        self.elements = []



    def circleHighlight(self, coords):
        # will take in an array of coordinates, draw low opacity circles 


        for c in coords:
            
            x = (ord(c[0]) - 96) * X_MULTIPLIER
            y =(9 - int(c[1])) * Y_MULTIPLIER

            # print(f"y = {y}")

            print(f"highlighting {x},{y}")

            new_element = Circle(x,y, self.screen)
            self.elements.append(new_element)
    


    def renderElements(self):

        for e in self.elements:
            e.render()
    


    def clearElements(self):
        for e in self.elements:
            del e
        self.elements = []