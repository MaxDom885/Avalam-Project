import tkinter as tk
from tkinter import messagebox
from tictactoe import TicTacToe
from minimax_player import best_move

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = TicTacToe()
        self.current_player = 'X'
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text='', font=('normal', 20), width=5, height=2,
                                    command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def on_button_click(self, i, j):
        position = i * 3 + j
        if self.board.make_move(self.current_player, position):
            self.buttons[i][j].config(text=self.current_player)
            if self.board.current_winner:
                messagebox.showinfo("Game Over", f"Player {self.board.current_winner} wins!")
                self.root.quit()
            elif self.board.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.root.quit()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.root.after(500, self.ai_move)  # Delay AI move for better UX

    def ai_move(self):
        move = best_move(self.board)
        i, j = divmod(move, 3)
        self.buttons[i][j].config(text='O')
        self.board.make_move('O', move)
        if self.board.current_winner:
            messagebox.showinfo("Game Over", f"Player {self.board.current_winner} wins!")
            self.root.quit()
        elif self.board.is_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.root.quit()
        self.current_player = 'X'

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
