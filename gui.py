# -*- coding: utf-8 -*-
"""
Graphical user interface for the Avalam game.
Copyright (C) 2010 - Vianney le Clément, UCLouvain
Some inspiration was taken from code by Pierre Schaus and Grégoire Dooms.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see http://www.gnu.org/licenses/.
"""

import threading
from tkinter import *
from tkinter.font import Font
from avalam import *
from game import Viewer

class TkViewer(Viewer):
    """Graphical viewer using Tk."""
    w = 55  # size of a cell
    r_hole = w // 6  # radius of a hole
    r_tower = w // 3  # radius of a tower

    def __init__(self, board):
        """Create a GUI viewer.

        Arguments:
        board -- initial board (a Board instance)
        """
        self.board = board
        self.canvas_width = self.w * board.columns
        self.canvas_height = self.w * board.rows
        self.barrier = threading.Event()
        self.root = Tk()
        self.root.title("Avalam")
        self.root.resizable(False, False)
        self.root.bind_all("<Escape>", self.close)
        self.font = Font(size=16)
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        # tower_ids is filled by _update_gui
        self.tower_ids = [[0 for j in range(self.board.columns)] for i in range(self.board.rows)]

        for i, j, h in self.board.get_towers():
            y = (i + .5) * self.w
            x = (j + .5) * self.w
            self.canvas.create_oval(x - self.r_hole, y - self.r_hole, x + self.r_hole, y + self.r_hole, width=2, outline="grey")
        self.status = Label(self.root, height=2, justify=LEFT)
        self.status.pack(side=LEFT)
        self.status_text = ""
        self.substatus_text = ""
        self.running = False

    def run(self):
        """Launch the GUI."""
        if self.running:
            return
        self.running = True
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        # ensure the main thread exits when closing viewer during human action
        self.root = None
        self.action = None  # generate invalid action
        self.barrier.set()

    def close(self, event=None):
        """Close the GUI."""
        if self.root is not None:
            self.root.destroy()

    def set_status(self, new_status):
        """Set the first line of the status bar."""
        s = self.status_text = new_status
        if self.substatus_text:
            s += f" \n {self.substatus_text}"
        self.status["text"] = s

    def set_substatus(self, new_substatus):
        """Set the second line of the status bar."""
        self.substatus_text = new_substatus
        self.set_status(self.status_text)

    def update(self, board, step):
        self.board = board
        if self.root is not None:
            self.root.after_idle(self._update_gui, board, step)

    def _update_gui(self, board, step):
        self.canvas.delete("towers")
        for i, j, h in board.get_towers():
            y = (i + .5) * self.w
            x = (j + .5) * self.w
            if h < 0:
                c = "red"
            else:
                c = "yellow"
            o = self.canvas.create_oval(x - self.r_tower, y - self.r_tower, x + self.r_tower, y + self.r_tower, fill=c, tags=["towers"])
            self.canvas.create_text(x, y, text=str(abs(h)), font=self.font, tags=["towers"])
            self.tower_ids[i][j] = o
            self._mark((i, j))  # ensure coherent unselected appearance
        if step % 2:
            player = "red"
        else:
            player = "yellow"
        self.set_status(f"Step {step}: {player}'s turn.")
        self.set_substatus("")

    def play(self, percepts, max_height, step, time_left):
        if self.root is None:
            return None
        if 1 - step % 2:
            self.player = "red"
        else:
            self.player = "yellow"
        self.barrier.clear()
        self.root.after_idle(self._play_start)
        self.barrier.wait()
        return self.action

    def _play_start(self):
        """Configure GUI to accept user input."""
        self.play_step = 1
        self.selection = None
        self.set_substatus("Selectionner une tour à déplacer ")
        self.canvas.bind("<Leave>", self._play_leave)
        self.canvas.bind("<Motion>", self._play_motion)
        self.canvas.bind("<Button-1>", self._play_click)
        self.canvas.event_generate("<Motion>")

    def _play_leave(self, event):
        """Handler for Mouse Leave event"""
        if event.state & 0x100:  # leave event is also called on mouse click
            return
        if self.selection is not None:
            if self.play_step != 2 or self.selection != self.action:
                self._mark(self.selection)
            self.selection = None

    def _play_motion(self, event):
        """Handler for Mouse Motion event"""
        self._play_leave(event)
        i, j = int(event.y / self.w), int(event.x / self.w)
        if i < 0 or i >= self.board.rows or j < 0 or j >= self.board.columns:
            return
        if (self.play_step == 1 and self.board.is_tower_movable(i, j)) or (self.play_step == 2 and self.action == (i, j)):
            self.selection = (i, j)
            self._mark(self.selection, "origin")
        elif self.play_step == 2 and self.action + (i, j) in self.moves:
            self.selection = (i, j)
            self._mark(self.selection, "destination")

    def _play_click(self, event):
        """Handler for Mouse Click event"""
        if self.selection is None:
            return
        i, j = self.selection
        if self.play_step == 1:
            # Select origin tower
            self._mark(self.selection, "origin")
            self.action = self.selection
            self.moves = list(self.board.get_tower_actions(i, j))
            self.play_step = 2
            self.set_substatus("Selectionner une tour ")
        elif self.play_step == 2 and self.selection == self.action:
            # Deselect origin tower
            self._play_start()
        elif self.play_step == 2:
            # Select destination tower
            action = self.action + (i, j)
            if action in self.moves:
                self._mark(self.action)
                self._mark(self.selection)
                self.action += self.selection
                self.set_substatus(" ")
                self.canvas.unbind("<Leave>")
                self.canvas.unbind("<Motion>")
                self.canvas.unbind("<Button-1>")
                self.barrier.set()

    def _mark(self, tower, style="unselected"):
        """Mark tower as unselected, origin or destination."""
        i, j = tower
        o = self.tower_ids[i][j]
        if style == "unselected":
            self.canvas.itemconfigure(o, outline="black", width=1)
        elif style == "origin":
            self.canvas.itemconfigure(o, outline="darkgreen", width=3)
        elif style == "destination":
            self.canvas.itemconfigure(o, outline="darkred", width=3)
        else:
            assert False

    def finished(self, board, steps, winner, reason=""):
        if self.root is None:
            return
        if winner == 0:
            s = "Match Nul"
        elif winner < 0:
            s = "red vainqueur "
        else:
            s = "yellow Vainqueur"
        s += f" après {steps} coups."
        self.root.after_idle(self.set_status, s)
        if reason:
            self.root.after_idle(self.set_substatus, reason)

    def replay(self, trace, show_end=False):
        """Replay a game given its saved trace.

        Attributes:
        trace -- trace of the game
        show_end -- start with the final state instead of the initial state
        """
        self.trace = trace
        # generate all boards to access them backwards
        self.boards = [trace.get_initial_board()]
        for action, t in trace.actions:
            b = self.boards[-1].clone()
            b.play_action(action)
            self.boards.append(b)

        if self.root is not None:
            self.root.after_idle(self._replay_gui, show_end)
            self.run()

    def _replay_gui(self, show_end):
        """Initialize replay UI"""
        self.b_next = Button(self.root, text=">", command=self._replay_next)
        self.b_play = Button(self.root, text="Play", command=self._replay_play)
        self.b_prev = Button(self.root, text="<", command=self._replay_prev)
        self.b_next.pack(side=RIGHT)
        self.b_play.pack(side=RIGHT)
        self.b_prev.pack(side=RIGHT)
        self.root.bind_all("<Left>", self._replay_prev)
        self.root.bind_all("<Right>", self._replay_next)
        self.root.bind_all("<Home>", self._replay_first)
        self.root.bind_all("<End>", self._replay_last)
        self.root.bind_all("<space>", self._replay_play)
        self.playing = False
        if show_end:
            self._replay_goto(len(self.boards) - 1)
        else:
            self._replay_goto(0)

    def _replay_goto(self, step):
        """Update UI to show step step."""
        self.step = step
        self._update_gui(self.boards[step], step)
        if step == len(self.boards) - 1:
            self.finished(self.boards[step], step, self.trace.winner, self.trace.reason)
        if self.playing:
            self.playing = False
            self.b_play["text"] = "Play"
        if self.playing:
            self.after_id = self.root.after(int(self.trace.actions[step][1] * 1000), self._replay_goto, step + 1)
        else:
            if step == 0:
                self.b_prev["state"] = DISABLED
            else:
                self.b_prev["state"] = NORMAL
            if step == len(self.boards) - 1:
                self.b_next["state"] = DISABLED
            else:
                self.b_next["state"] = NORMAL

    def _replay_next(self, event=None):
        if not self.playing and self.step < len(self.boards) - 1:
            self._replay_goto(self.step + 1)

    def _replay_prev(self, event=None):
        if not self.playing and self.step > 0:
            self._replay_goto(self.step - 1)

    def _replay_first(self, event=None):
        if not self.playing:
            self._replay_goto(0)

    def _replay_last(self, event=None):
        if not self.playing:
            self._replay_goto(len(self.boards) - 1)

    def _replay_play(self, event=None):
        if self.playing:
            self.root.after_cancel(self.after_id)
            self.playing = False
            self.b_play["text"] = "Play"
            self._replay_goto(self.step)
        else:
            self.playing = True
            self.b_prev["state"] = DISABLED
            self.b_next["state"] = DISABLED
            self.b_play["text"] = "Pause"
            if self.step < len(self.boards) - 1:
                self._replay_goto(self.step)
            else:
                self._replay_goto(0)
