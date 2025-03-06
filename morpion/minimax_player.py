from tictactoe import TicTacToe

def minimax(board, depth, maximizing_player):
    if board.check_winner('X'):
        return 1
    if board.check_winner('O'):
        return -1
    if board.is_full():
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.available_moves():
            board.make_move('X', move)
            eval = minimax(board, depth + 1, False)
            board.make_move(' ', move)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.available_moves():
            board.make_move('O', move)
            eval = minimax(board, depth + 1, True)
            board.make_move(' ', move)
            min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_value = float('-inf')
    best_move = None
    for move in board.available_moves():
        board.make_move('X', move)
        move_value = minimax(board, 0, False)
        board.make_move(' ', move)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move
