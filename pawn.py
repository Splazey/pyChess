from piece import Piece
import pygame
from queen import Queen

BLACK = "black\pawn.png"
WHITE = "white\pawn.png"

X_MULTIPLIER = 100
Y_MULTIPLIER = 100
OFFSET = 100


class Pawn(Piece):


    def __init__(self, screen, color, x, y):
        super().__init__(screen, x, y)

        self.firstMove = True

        if color == 'b':
            self.p = BLACK
            self.white = False
        else:
            self.p = WHITE
            self.white = True

        self.img = pygame.image.load(self.p).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (100, 100))

    def revokeDoubleStep(self):
        self.firstMove = False

    def checkLegal(self, x, y, board):




        legal = []

        if self.firstMove:
            step = [1,2]

        else: 
            step = [1]
        
        if self.white: # the pawn is white
            for i in range(len(step)):
                step[i] = step[i] * -1



        

        for b in board:
            print(b)


        for i in step: # check forward
            if y+i >= 0 and y+i < 8 and board[y + i][x] == '.':
                legal.append(chr(x + 97) + str((9 - y) - i - 1))



        # check the right side for a capturable opponent piece
        if x + 1 < 8 and isinstance(board[y + step[0]][x + 1], Piece) and board[y + step[0]][x + 1].white != self.white:
            legal.append(chr(x + 1 + 97) + str((9 - y) - step[0] - 1))

        # check the left side for a capturable opponent piece
        if x - 1 >= 0 and isinstance(board[y + step[0]][x - 1], Piece) and board[y + step[0]][x - 1].white != self.white:
            legal.append(chr(x - 1 + 97) + str((9 - y) - step[0] - 1))



        print(f"legal moves: {legal}")
        return legal


    def __del__(self):
        pass

    def promote(self): # pawn promotion code, called in the board class when the pawn hits the end of the board

        x = int((self.x - OFFSET) / X_MULTIPLIER)
        y = int((self.y - OFFSET) / Y_MULTIPLIER)



        if self.white:
            color = 'w'
        else:
            color = 'b'

        promoted = Queen(self.screen, color, x, y) # TODO implement support for letting the user pick the piece to promote to 

        return promoted # return the new, promoted piece
        