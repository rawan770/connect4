import math
import random
from board_structure import *
from Minimax import *
from winning_move import winning_move    # <-- ده السطر اللي كان عامل المشكلة وصلحناه

def player_click(self, event):
    if self.game_over or self.turn != PLAYER:
        return

    col = event.x // SQUARESIZE

    if is_valid_location(self.board, col):
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, PLAYER_PIECE)

        if winning_move(self.board, PLAYER_PIECE):
            self.show_winner("Player")
            self.draw_board()
        elif len(get_valid_locations(self.board)) == 0:
            self.show_winner("Draw")
            self.draw_board()
        else:
            self.turn = AI
            self.draw_board()
            if not self.game_over:
                self.root.after(500, self.ai_move)

def ai_move(self):
    if self.game_over:
        return

    if len(get_valid_locations(self.board)) == 0:
        self.show_winner("Draw")
        return

    col, minimax_score = minimax(self.board, 4, -math.inf, math.inf, True)

    if col is not None and is_valid_location(self.board, col):
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, AI_PIECE)

        if winning_move(self.board, AI_PIECE):
            self.show_winner("AI")
        elif len(get_valid_locations(self.board)) == 0:
            self.show_winner("Draw")
        else:
            self.turn = PLAYER

        self.draw_board()
