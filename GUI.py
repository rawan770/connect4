
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys
import math
import random
from board_structure import *
import winning_move
import position_scoring
import Minimax
import Player_Clickand_AI_Move
class Connect4GUI:

    def __init__(self, root):
        self.root = root
        self.board = create_board()
        self.turn = random.randint(PLAYER, AI)
        self.game_over = False

        self.canvas = tk.Canvas(root, width=COLUMN_COUNT * SQUARESIZE, height=(ROW_COUNT + 1) * SQUARESIZE, bg="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.player_click)
        self.draw_board()

        if self.turn == AI:
            self.root.after(500, self.ai_move)
    def player_click(self, event):
        Player_Clickand_AI_Move.player_click(self, event)

    def ai_move(self):
        Player_Clickand_AI_Move.ai_move(self)
    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                x0 = c * SQUARESIZE
                y0 = (ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE  # تعديل الإحداثيات لتناسب الـ GUI
                x1 = x0 + SQUARESIZE
                y1 = y0 + SQUARESIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=BLUE, outline=BLACK)

                piece = self.board[r][c]
                color = BLACK
                if piece == PLAYER_PIECE:
                    color = RED
                elif piece == AI_PIECE:
                    color = YELLOW
                self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill=color, outline=BLACK)
        self.root.update()

    def show_winner(self, winner_name):
        color = RED if winner_name == "Player" else YELLOW
        if winner_name == "Draw":
            msg = "It's a Draw!"
            color = "white"
        else:
            msg = f"{winner_name} Wins!"

        messagebox.showinfo("Game Over", msg)
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            SQUARESIZE // 2,
            text=msg,
            font=("monospace", 40),
            fill=color
        )
        self.game_over = True
if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4GUI(root)
    root.mainloop()        
