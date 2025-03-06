import random
from common import Player, InvalidAction, serve_player, player_main
from avalam import Board

class RandomPlayer(Player):
    """A random Avalam player."""

    def play(self, percepts, max_height, step, time_left):
        """Play and return a random action."""
        board = Board(percepts, max_height)
        actions = list(board.get_actions())
        if not actions:
            raise InvalidAction("No valid actions available")
        return random.choice(actions)

if __name__ == "__main__":
    def options_cb(player, parser):
        parser.add_option("-p", "--port", type="int", dest="port", default=8000, help="set port number (default: %default)")

    def setup_cb(player, parser, options):
        pass

    player_main(RandomPlayer(), options_cb, setup_cb)
