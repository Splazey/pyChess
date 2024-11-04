import pygame
from circle import Circle
from square import Square
from piece import Piece
from king import King

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
    
    def captureHighlight(self, coords):
        # will take in an array of coordinates, draw low opacity circles 


        for c in coords:
            
            x = (ord(c[0]) - 96) * X_MULTIPLIER
            y =(9 - int(c[1])) * Y_MULTIPLIER

            print(f"square highlighting {x},{y}")

            new_element = Square(x,y, self.screen)
            self.elements.append(new_element)

    def highlightMovements(self, coords, board):

        circles = []
        squares = []

        for c in coords:
            x = (ord(c[0]) - 96) - 1
            y = (9 - int(c[1])) - 1

            if isinstance(board[y][x], Piece):
                squares.append(c)
            else:
                circles.append(c)
        
        self.circleHighlight(circles)
        self.captureHighlight(squares)

    def checkHighlight(self, board):

        whiteCoverage = []
        blackCoverage = []

        whiteKing = []
        blackKing = []

        for row in board:
            for tile in row:
                if isinstance(tile, King):
                    if tile.white:
                        whiteKing.append()
                    else:
                        pass
                elif isinstance(tile, Piece) and tile.white:
                    whiteCoverage.extend(tile.checkLegal())
                elif isinstance(tile, Piece) and not tile.white:
                    blackCoverage.extend(tile.checkLegal())

    def renderElements(self):

        for e in self.elements:
            e.render()
    


    def clearElements(self):
        for e in self.elements:
            del e
        self.elements = []