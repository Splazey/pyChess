
import pygame
from piece import Piece


BLACK = "black\king.png"
WHITE = "white\king.png"



class King(Piece):


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

        self.playing = False


    def getCheckTiles(self, board):
        y = 0
        ct = []
        for row in board:
            x = 0
            for tile in row:
                if isinstance(tile, Piece) and tile.white != self.white:
                    # print(f"{type(tile)} on {x},{y}")
                    if isinstance(tile, King) and tile.playing == True:
                        continue
                    ct.extend(tile.checkLegal(x,y,board))
                x += 1
            y += 1
        return ct
    

    def isSafe(self, location, danger):
        return not location in danger

    def checkLegal(self, x, y, board):
        self.playing = True
        ct = self.getCheckTiles(board)


        legal = []


        directions = [ # the 8 directions a king can move through
            [1,0],
            [-1,0],
            [0,-1],
            [0,1],
            [1,-1],
            [1,1],
            [-1,-1],
            [-1,1]
        ]


        for d in directions:

            x_offset = d[0]
            y_offset = d[1]


            if 0 <= x + x_offset < 8 and 0 <= y + y_offset < 8:
                # print(f"checking {chr(x + x_offset + 97) + str((9 - y) - y_offset - 1)}")
                if board[y + y_offset][x + x_offset] == '.' or (isinstance(board[y + y_offset][x + x_offset], Piece) and board[y + y_offset][x + x_offset].white != self.white):
                    # if it is an empty tile, or a tile in which an enemy is in
                    if self.isSafe(chr(x + x_offset + 97) + str((9 - y) - y_offset - 1), ct):
                        legal.append(chr(x + x_offset + 97) + str((9 - y) - y_offset - 1)) # add that tile to the legal moves array

        self.playing = False

        print(f"Legal moves: {legal}")
        return legal