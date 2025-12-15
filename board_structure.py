import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
import math

# ----------------- Constants -----------------
BLUE = "#0000FF"
BLACK = "#000000"
RED = "#FF0000"
YELLOW = "#FFFF00"

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
SQUARESIZE = 100
RADIUS = SQUARESIZE//2 - 5

# ----------------- Board Functions -----------------


def create_board():
    return np.zeros((ROW_COUNT,COLUMN_COUNT))




def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]



