import copy
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King

# Board object class that stores pieces, and inputs and outputs FEN

# the board will use the piece objects, while the main program will use the board

# when a piece is picked, the main program communicates with the piece, the board should only keep a low opacity copy of the piece in its initial pos

from piece import Piece

X_DIVISOR = 100
Y_DIVISOR = 100
OFFSET = 1





class Board:


    def __init__(self, screen):


        self.b = []
        self.screen = screen
        self.moving = False

        for i in range(8):
            self.b.append(['.','.','.','.','.','.','.','.'])

        self.printBoard()


    def printBoard(self): # method used for debugging, prints the board to the terminal
        
        for row in self.b:
            for cell in range(8):
                print(f"  {row[cell]}",end="")
            print()

    def getFEN():
        pass

    def setFEN(self, code):
        y = 0
        x = 0
        for char in code:
            print(f"-------------- NOW: {char}")
            print(f"Y ={y}")
            if char.isdigit(): # it is a digit
                x += int(char)
                # print(f"x now: {x}")
            elif char.isalpha(): # it is a letter
                
                if char.isupper():
                    clr = 'w'
                else:
                    clr = 'b'
                
                if char.lower() == 'p':
                    new_piece = Pawn(self.screen, clr)
                elif char.lower() == 'r':
                    new_piece = Rook(self.screen, clr)
                elif char.lower() == 'n':
                    new_piece = Knight(self.screen, clr)
                elif char.lower() == 'b':
                    new_piece = Bishop(self.screen, clr)
                elif char.lower() == 'q':
                    new_piece = Queen(self.screen, clr)
                elif char.lower() == 'k':
                    new_piece = King(self.screen, clr)
                
                self.b[y][x] = new_piece
                print(f"x is {x + 97}")
                print(f"y is {y}")

                new_piece.goto(str(chr(x + 97)) + str(8 - y))

                print(f"Piece spawned in {str(chr(x + 97)) + str(8 - y)}")

                x += 1
                print(f"x= {x}")
            else: # it is a slash
                print("RESET X")
                y += 1
                x = 0
    
    def toggleMoving(self):
        self.moving = not self.moving


    def renderPieces(self):
        for row in self.b:
            for cell in row:
                if isinstance(cell, Piece):
                    cell.render()

    def getPieces(self):
        return self.pieces

    # def render(self):

    #     if self.moving: # if the user is moving a piece
    #         for tile in self.b:
    #             if isinstance(tile, Piece): # TODO: once all the pieces are done, check later if this would work with children classes of Piece
    #                 pass


    def getTile(self, x, y):
        #TODO: get click coordinates and return a proper location system for the coordinates (e.g. "b5")
        print(f"{y + OFFSET}/{Y_DIVISOR}={round((y + OFFSET)/ Y_DIVISOR)}") 
        return chr(int(round((x - OFFSET)/ Y_DIVISOR)) + 96) + str(9 - int(round((y + OFFSET)/ Y_DIVISOR))) # works for now
    


