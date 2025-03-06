import random
from common import Player, InvalidAction, serve_player, player_main
from avalam import Board

class MyAvalamPlayer(Player):
    """A basic Avalam player."""

    def __init__(self):
        self.depth = float('inf')

    def eval_fn(self, state):
        """Evaluation function. Return an evaluation of state."""
        player, board = state
        # TODO: Implement a better evaluation function
        return board.get_winner()

    def cutoff_test(self, state, depth):
        """Cut-off test. Return True to stop at this node."""
        player, board = state
        return board.is_finished() or depth >= self.depth

    def play(self, percepts, max_height, step, time_left):
        """Play and return an action."""
        board = Board(percepts, max_height)
        actions = list(board.get_actions())
        if not actions:
            raise InvalidAction("No valid actions available")
        return random.choice(actions)

if __name__ == "__main__":
    def options_cb(player, parser):
        parser.add_option("-p", "--port", type="int", dest="port", default=8000, help="set port number (default: %default)")
        parser.add_option("-d", "--depth", type="int", dest="depth", default=-1, help="set search depth (default: infinite)")

    def setup_cb(player, parser, options):
        if options.depth >= 0:
            player.depth = options.depth

    player_main(MyAvalamPlayer(), options_cb, setup_cb)
