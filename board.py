import copy
import pygame
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
        self.srcX = -1
        self.srcY = -1

        for i in range(8):
            self.b.append(['.','.','.','.','.','.','.','.'])

        self.brd = pygame.image.load("board.png")
        self.brd = pygame.transform.smoothscale(self.brd, (self.screen.get_width(),self.screen.get_height()))

        # self.printBoard()


    def blitBoard(self):
        self.screen.blit(self.brd, (0,0))

    def printBoard(self): # method used for debugging, prints the board to the terminal
        
        for row in self.b:
            for cell in range(8):
                if isinstance(row[cell], Piece):
                    print("  p", end="")
                else:
                    print(f"  {row[cell]}",end="")
            print()

    def getFEN():
        pass

    def setFEN(self, code):
        y = 0
        x = 0
        for char in code: # iterate through each character of the FEN code
            if char.isdigit(): 
                x += int(char) # increase x by the number shown in the code
           
           
            elif char.isalpha(): # it is a character, therefore it represents a piece on the board
                
                if char.isupper(): # depending on if the character is capital or small, it determines wether the piece is black or white
                    color = 'w'
                else:
                    color = 'b'
                

                if char.lower() == 'p':
                    new_piece = Pawn(self.screen, color, x, y)
                elif char.lower() == 'r':
                    new_piece = Rook(self.screen, color, x, y)
                elif char.lower() == 'n':
                    new_piece = Knight(self.screen, color, x, y)
                elif char.lower() == 'b':
                    new_piece = Bishop(self.screen, color, x, y)
                elif char.lower() == 'q':
                    new_piece = Queen(self.screen, color, x, y)
                elif char.lower() == 'k':
                    new_piece = King(self.screen, color, x, y)
                
                self.b[y][x] = new_piece

                # new_piece.goto(str(chr(x + 97)) + str(8 - y), [])

                # self.printBoard()


                x += 1
            
            
            else: # it is a slash, therefore, go to the next row of the board
                y += 1
                x = 0
    
    def toggleMoving(self, inner, outer):
        self.moving = not self.moving
        self.srcX = outer
        self.srcY = inner


    def renderPieces(self):
        for row in self.b:
            for cell in row:
                if isinstance(cell, Piece):
                    cell.render()

    def getPieces(self):
        return self.pieces

    def getTile(self, x, y): # based on the click position, calculates the tile that the user clicked on
        # print(f"{yc + OFFSET}/{Y_DIVISOR}={round((yc + OFFSET)/ Y_DIVISOR)}") 
        xc = int(round((x - OFFSET)/ Y_DIVISOR))
        yc = 9 - int(round((y + OFFSET)/ Y_DIVISOR))

        print(f"xc = {xc}")
        print(f"yc = {yc}")

        if xc <= 8 and xc > 0 and yc <= 8 and  yc > 0:
            return chr(xc + 96) + str(yc) # works for now
        return "x0" # return an invalid coordinate indicator





    def movePiece(self, x, y, turn): 

        c = self.getTile(x,y)

        inner = (97 - ord(c[0])) * -1
        outer = 8 - int(c[1])

        if inner == 23:
            print("Invalid position clicked.")
            return

        print(f"clicked on coords: {outer},{inner}, aka {c}")


        if self.moving: # x and y here will refer to DESTINATION

            # if the player has already selected a piece and is trying to select its destination
            # also checks if the destination position is empty, or is for an enemy team


                
            # if self.b[inner][outer] != '.' and self.b[inner][outer].white != turn:
            #     print("opponent piece selected")
            if not self.b[self.srcY][self.srcX].goto(c, self.b): # execute the goto function, involves checking whether the move is legal or not
                print("returning false to the driver")
                self.toggleMoving(-1, -1)
                return False # return a false message to the program that a move has not been made yet
            

            # TODO call checkCheck() if the moved piece was a king
            


            # move the piece to the clicked position
            if isinstance(self.b[outer][inner], Piece):
                print(f"piece in {c} was deleted.")
            self.b[outer][inner] = self.b[self.srcY][self.srcX]

            print(f"king would now be in {self.getTile(self.srcX, self.srcY)}")

            # special conditions if the piece that was moved is a pawn
            if isinstance(self.b[self.srcY][self.srcX], Pawn):
                
                self.b[self.srcY][self.srcX].revokeDoubleStep() # revoke the double step attribute

                if outer == 0 or outer == 7: # if the pawn has hit the end of the board, promote the pawn
                    print("Promotion!")
                    self.b[outer][inner] = self.b[self.srcY][self.srcX].promote()




            self.b[self.srcY][self.srcX] = '.' # set the initial position to empty

            print(f"Piece moved to {c}")
            self.printBoard()

            self.toggleMoving(-1, -1)

            return True # return a true message to the driver program, indicating that a move has been made
        
        elif isinstance(self.b[outer][inner], Piece) and self.b[outer][inner].white == turn: # x and y here will refer to SOURCE
            # check if the clicked coordinates have a piece in them, and if the piece matches the turn specified by the driver program
            
            print(f"{self.b[outer][inner]} is now being moved")
            self.toggleMoving(outer, inner) # srcX and srcY are updated here




            return False # return a false message to the driver program, indicating that a move has not been made yet
        
        
        return False