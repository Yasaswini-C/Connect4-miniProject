# from pydoc import cram
# from re import S
# from select import select
# from turtle import Screen, width
from ctypes.wintypes import RGB
# from turtle import color
import numpy as np
import pygame
import sys
import math

BLACK = RGB(0, 0, 0)
BLUE = RGB(255,255,220)
RED = RGB(94, 105, 225)
YELLOW = RGB(0, 215, 225)

ROW_COUNT = 6
COL_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board

def drop_piece(board, row, col, player):
    board[row][col] = player

def is_valid_location(board, col):
    if board[ROW_COUNT-1][col] == 0:
        return True
    else:
        return False

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+2][c+3] == piece:
                return True

    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE//2), RADIUS)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE+SQUARESIZE//2, height - (r*SQUARESIZE+SQUARESIZE//2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c*SQUARESIZE+SQUARESIZE//2, height - (r*SQUARESIZE+SQUARESIZE//2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE//2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

pygame.font.init()
# print(pygame.font.get_fonts())
# myfont = pygame.font.Font(pygame.font.get_default_font(), 75)
myfont = pygame.font.SysFont('avenir', 55)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (x, SQUARESIZE//2), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (x, SQUARESIZE//2), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            if turn == 0:
                x = event.pos[0]
                selection = int(math.floor(x // SQUARESIZE))
                # int(input("Player 1 Make your selection(0-6): "))
                if is_valid_location(board, selection):
                    row = get_next_open_row(board, selection)
                    drop_piece(board, row, selection, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player1 WINS", False, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
            else:
                x = event.pos[0]
                selection = int(math.floor(x // SQUARESIZE))

                if is_valid_location(board, selection):
                    row = get_next_open_row(board, selection)
                    drop_piece(board, row, selection, 2)

                    if winning_move(board, 2):
                        # print("Player2 WINS")
                        label = myfont.render("Player2 WINS", False, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
