
import pygame
from piece import Piece

BLACK = "black\knight.png"
WHITE = "white\knight.png"


class Knight(Piece):


    def __init__(self, screen, color, x, y):
        super().__init__(screen, x, y)

        if color == 'b':
            self.p = BLACK
            self.white = False
        else:
            self.p = WHITE
            self.white = True
    
        self.img = pygame.image.load(self.p).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (100, 100))

    def checkLegal(self, x, y, board):
        
        legal = []
        directions = [ # The eight tiles a knight can travel to
            [2,1],
            [1,2],
            [-2,1],
            [-1,2],
            [-2,-1],
            [-1,-2],
            [1,-2],
            [2,-1]
        ]


        for d in directions:

            x_offset = d[0]
            y_offset = d[1]


            if 0 <= x + x_offset < 8 and 0 <= y + y_offset < 8:
                if board[y + y_offset][x + x_offset] == '.' or (isinstance(board[y + y_offset][x + x_offset], Piece) and board[y + y_offset][x + x_offset].white != self.white):
                    # if it is an empty tile, or a tile in which an enemy is in
                    legal.append(chr(x + x_offset + 97) + str((9 - y) - y_offset - 1)) # add that tile to the legal moves array
            



        print(f"Legal moves: {legal}")
        return legal