from tictactoe import TicTacToe
from minimax_player import best_move

def play_game():
    board = TicTacToe()
    current_player = 'X'

    while not board.current_winner and not board.is_full():
        board.print_board()
        if current_player == 'X':
            move = int(input("Enter your move (0-8): "))
            if not board.make_move(current_player, move):
                print("Invalid move. Try again.")
                continue
        else:
            move = best_move(board)
            board.make_move(current_player, move)
            print(f"Computer plays {move}")

        current_player = 'O' if current_player == 'X' else 'X'

    board.print_board()
    if board.current_winner:
        print(f"Player {board.current_winner} wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()
