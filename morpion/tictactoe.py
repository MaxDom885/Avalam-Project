class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, player, position):
        if self.board[position] == ' ':
            self.board[position] = player
            if self.check_winner(player):
                self.current_winner = player
            return True
        return False

    def check_winner(self, player):
        # Check rows, columns, and diagonals
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        return any(all(self.board[p] == player for p in condition) for condition in win_conditions)

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def heuristic(self):
        x2 = sum(all(self.board[p] == 'X' for p in condition) for condition in [
            [0, 1], [1, 2], [3, 4], [4, 5], [6, 7], [7, 8], [0, 3], [3, 6], [1, 4], [4, 7], [2, 5], [5, 8], [0, 4], [4, 8], [2, 4]
        ])
        x1 = sum(all(self.board[p] == 'X' for p in condition) for condition in [
            [0], [1], [2], [3], [4], [5], [6], [7], [8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
        ])
        o2 = sum(all(self.board[p] == 'O' for p in condition) for condition in [
            [0, 1], [1, 2], [3, 4], [4, 5], [6, 7], [7, 8], [0, 3], [3, 6], [1, 4], [4, 7], [2, 5], [5, 8], [0, 4], [4, 8], [2, 4]
        ])
        o1 = sum(all(self.board[p] == 'O' for p in condition) for condition in [
            [0], [1], [2], [3], [4], [5], [6], [7], [8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
        ])
        return 3 * x2 + 2 * x1 - (3 * o2 + 2 * o1)

    def is_full(self):
        return ' ' not in self.board
