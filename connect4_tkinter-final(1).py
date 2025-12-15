#member1
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



#member2
def winning_move(board, piece):
    # Horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i]==piece for i in range(4)):
                return True
    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c]==piece for i in range(4)):
                return True
    # Diagonal /
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c+i]==piece for i in range(4)):
                return True
    # Diagonal \
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i]==piece for i in range(4)):
                return True
    return False

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


#member3

# ----------------- AI Functions (Evaluation Logic) -----------------
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # --- التعديل الجوهري هنا ---
    # لو الخصم (اللاعب) عنده 3 قطع ومكان فاضي، دي مصيبة!
    # نقصنا السكور بـ 100 عشان الـ AI يخاف ويجري يقفل الطريق
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 100  
    
    return score

def score_position(board, piece):
    score = 0
    # تفضيل اللعب في المنتصف (Center Column)
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # تقييم الصفوف
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # تقييم الأعمدة
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # تقييم الأقطار الموجبة
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # تقييم الأقطار السالبة
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

#member4
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves (Draw)
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    
    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else: # Minimizing player
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


#member5
# ----------------- GUI -----------------
class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.board = create_board()
        self.turn = random.randint(PLAYER, AI)
        self.game_over = False

        self.canvas = tk.Canvas(root, width=COLUMN_COUNT*SQUARESIZE, height=(ROW_COUNT+1)*SQUARESIZE, bg="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.player_click)
        self.draw_board()

        if self.turn == AI:
            self.root.after(500, self.ai_move)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                x0 = c*SQUARESIZE
                y0 = (ROW_COUNT - 1 - r)*SQUARESIZE + SQUARESIZE # تعديل الإحداثيات لتناسب الـ GUI
                x1 = x0 + SQUARESIZE
                y1 = y0 + SQUARESIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=BLUE, outline=BLACK)

                piece = self.board[r][c]
                color = BLACK
                if piece == PLAYER_PIECE:
                    color = RED
                elif piece == AI_PIECE:
                    color = YELLOW
                self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=color, outline=BLACK)
        self.root.update()

    def show_winner(self, winner_name):
        color = RED if winner_name=="Player" else YELLOW
        if winner_name == "Draw":
            msg = "It's a Draw!"
            color = "white"
        else:
            msg = f"{winner_name} Wins!"
            
        messagebox.showinfo("Game Over", msg)
        self.canvas.create_text(
            self.canvas.winfo_width()//2, 
            SQUARESIZE//2, 
            text=msg, 
            font=("monospace", 40), 
            fill=color
        )
        self.game_over = True


#member6
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

        # Minimax call
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

# ----------------- Main -----------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect 4 - Tkinter AI")
    gui = Connect4GUI(root)
    root.mainloop()