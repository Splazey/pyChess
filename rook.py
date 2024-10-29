
import pygame
from piece import Piece

BLACK = "black\\rook.png"
WHITE = "white\\rook.png"


class Rook(Piece):


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




        # [x_offset, y_offset, pos, inc_x]
        directions = [
            [1,0], 
            [-1, 0], 
            [0, 1], 
            [0, -1]
            ]


        for d in directions:
            
            x_offset = d[0]
            y_offset= d[1]

            if x_offset == -1 or y_offset == -1:
                pos = False

            while 0 <= y + y_offset < 8 and 0 <= x + x_offset < 8:
                if isinstance(board[y + y_offset][x + x_offset], Piece):
                    print(f"Blocking Piece! in {chr(x + x_offset + 97) + str((9 - y) - y_offset - 1)}")

                    if board[y + y_offset][x + x_offset].white != self.white:
                        # the blocking piece is an enemy piece
                        print("enemy in range!")
                        legal.append(chr(x + x_offset + 97) + str((9 - y) - y_offset - 1))
                    break # stop exploring further since there is a blocking piece
                else:
                    legal.append(chr(x + x_offset + 97) + str((9 - y) - y_offset - 1))
                    
                    x_offset += d[0]
                    y_offset += d[1]



        
        print(f"legal moves: {legal}")
        return legal
