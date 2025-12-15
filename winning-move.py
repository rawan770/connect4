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
