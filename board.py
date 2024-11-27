
# Board class that stores pieces, and inputs and outputs FEN
# the board will use the piece objects, while the main program will use the board
# when a piece is picked, the main program communicates with the piece for move validation,
# the board class also communicates with the Highlighter class 
# to show the legal moves to the user once a piece is selected


# main library importing
import pygame
from highlighter import Highlighter


# pieces importing
from piece import Piece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King


# variables for coordinates control of board elements
X_DIVISOR = 100
Y_DIVISOR = 100
OFFSET = 1





class Board:


    def __init__(self, screen):


        self.b = [] # 2D array to store the board pieces, empty tiles are denoted by "."

        self.screen = screen
        self.h = Highlighter(self.screen) # Highlighter object, used by the board to highlight legal moves
        self.moving = False

        # X and Y coordinates variables to store the position of the piece that has been previously selected
        self.srcX = -1
        self.srcY = -1


        # initialize the board by making it empty
        for i in range(8):
            self.b.append(['.','.','.','.','.','.','.','.'])

        # load the board image (board.png)
        self.brd = pygame.image.load("board.png")
        self.brd = pygame.transform.smoothscale(self.brd, (self.screen.get_width(),self.screen.get_height()))

    def blitBoard(self): # Function to only blit the board at the background
        self.screen.blit(self.brd, (0,0))

    def printBoard(self): # Debugging function used to print the board position to the terminal, any pieces are indicated by a "p"
        
        for row in self.b:
            for cell in range(8):
                if isinstance(row[cell], Piece):
                    print("  p", end="")
                else:
                    print(f"  {row[cell]}",end="")
            print()

    def getFEN(): # Function to return the FEN code of the current board position
        # TODO: complete this function
        pass

    def setFEN(self, code): # modifies the board array to have the same position as the FEN code specified in the argument
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

                x += 1
            
            
            else: # it is a slash, therefore, go to the next row of the board
                y += 1
                x = 0
    
    def toggleMoving(self, inner, outer): # toggles the state of the board from selection mode to moving mode
        
        self.moving = not self.moving
        
        # Update the selected (source) piece positions
        self.srcX = outer
        self.srcY = inner


    def renderPieces(self): # Function to call the render() function all piece objects on the board array
        for row in self.b:
            for cell in row:
                if isinstance(cell, Piece):
                    cell.render()


    def renderHighlights(self): # Function to call renderElements() for the highlighter of the board
        self.h.renderElements()


    def getTile(self, x, y): # Function to convert screen coordinates to chess tile coordinates (e.g. "b4")
        
        xc = int(round((x - OFFSET)/ Y_DIVISOR))
        yc = 9 - int(round((y + OFFSET)/ Y_DIVISOR))


        if xc <= 8 and xc > 0 and yc <= 8 and  yc > 0:
            return chr(xc + 96) + str(yc)
        
        return "x0" # return an invalid coordinate indicator





    def movePiece(self, x, y, turn): # Function to handle piece movement, as well as highlighting legal moves once a piece has been selected

        # This function works in two modes, the mode is determined based on self.moving.
        # When a player selects a piece to move, self.moving is set to true, legal moves are highlighted
        # When a player moves the piece, the goto() function is called for the piece selected (indicated by self.srcX and self.srcY)

        c = self.getTile(x,y) # convert the given click coordinates into a chess tile coordinate 
        if c == "x0":
            return False
        
        # Generate inner and outer, indexes that point to the array (self.b) position that points to the piece that has been clicked
        inner = (97 - ord(c[0])) * -1
        outer = 8 - int(c[1])

        if self.moving: # x and y here will refer to DESTINATION
            # if the player has already selected a piece and is trying to select its destination
            # also checks if the destination position is empty, or is occupied by an opponent piece


            if self.srcX == -2:
                self.h.clearElements()

                legal = self.b[outer][inner].checkLegal(inner, outer, self.b)
                self.h.highlightMovements(legal, self.b)

                return False

            # in case the player chooses to move a different piece
            if isinstance(self.b[outer][inner], Piece) and self.b[outer][inner].white == turn:

                # edit the source to become the new piece that was selected
                self.srcX = inner
                self.srcY = outer

                self.h.clearElements()

                legal = self.b[outer][inner].checkLegal(inner, outer, self.b) # store the coordinates of the legal moves

                self.h.highlightMovements(legal, self.b)

                return False # Abort the function call, since another movePiece() will be called by the driver for the different picked piece

                
            if not self.b[self.srcY][self.srcX].goto(c, self.b): # execute the goto function, involves checking whether the move is legal or not
                # print("returning false to the driver")
                
                self.toggleMoving(-1, -1)
        
                self.h.clearElements()

                return False # return a false message to the program that a move has not been made yet
            

            # TODO call checkCheck() if the moved piece was a king
            


            # move the piece to the clicked position
            # if isinstance(self.b[outer][inner], Piece):
            #     print(f"piece in {c} was deleted.")
            self.b[outer][inner] = self.b[self.srcY][self.srcX]

            # print(f"king would now be in {self.getTile(self.srcX, self.srcY)}")

            # special conditions if the piece that was moved is a pawn
            if isinstance(self.b[self.srcY][self.srcX], Pawn):
                
                self.b[self.srcY][self.srcX].revokeDoubleStep() # revoke the double step attribute

                if outer == 0 or outer == 7: # if the pawn has hit the end of the board, promote the pawn
                    # print("Promotion!")
                    self.b[outer][inner] = self.b[self.srcY][self.srcX].promote()




            self.b[self.srcY][self.srcX] = '.' # set the initial position to empty



            self.toggleMoving(-1, -1) # declare that the move has been made

            self.h.clearElements() # clear the highlighting made for the legal moves, since the move has already been made

            return True # return a true message to the driver program, indicating that a move has been made
        
        elif isinstance(self.b[outer][inner], Piece) and self.b[outer][inner].white == turn: # x and y here will refer to SOURCE
            # check if the clicked coordinates have a piece in them, and if the piece matches the turn specified by the driver program
            
            self.toggleMoving(outer, inner) # srcX and srcY are updated here

            legal = self.b[outer][inner].checkLegal(inner, outer, self.b)

            self.h.highlightMovements(legal, self.b)

            return False # return a false message to the driver program, indicating that a move has not been made yet
        
        return False