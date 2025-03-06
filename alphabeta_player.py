import random
from avalam import *
import games
from player import player_main
from utils import *

class AvalamGame(games.Game):
    """Jeu Avalam.

    Un état est un tuple (p, b) où p est le joueur qui doit jouer et b est le plateau.
    """
    def legal_moves(self, state):
        # Retourne les actions légales disponibles pour le joueur actuel.
        return state[1].get_actions()

    def make_move(self, move, state):
        # Applique un coup au plateau et retourne le nouvel état.
        b = state[1].clone()
        b.play_action(move)
        return (state[0] > 0 and -1 or 1, b)

    def utility(self, state, player):
        # Calcule la valeur utilitaire de l'état pour un joueur donné.
        return player * state[1].get_winner()

    def terminal_test(self, state):
        # Teste si l'état est terminal (partie terminée).
        return state[1].is_finished()

    def to_move(self, state):
        # Retourne le joueur dont c'est le tour.
        return state[0]

    def successors(self, state):
        # Retourne les successeurs de l'état actuel sous forme d'actions et d'états résultants.
        # TODO changer l'implémentation par défaut
        return {(move, self.make_move(move, state)) for move in self.legal_moves(state)}

class AlphaBetaPlayer(Player):
    """Un joueur Avalam utilisant Alpha-Beta."""
    def __init__(self):
        self.depth = float('inf')  # Profondeur de recherche infinie par défaut.

    def eval_fn(self, state):
        """Fonction d'évaluation. Retourne une évaluation de l'état."""
        player, board = state
        # TODO changer l'implémentation par défaut
        return board.get_winner()

    def cutoff_test(self, state, depth):
        """Test de coupure. Retourne True pour arrêter l'exploration à ce nœud."""
        player, board = state
        # TODO changer l'implémentation par défaut
        return board.is_finished() or depth >= self.depth

    def play(self, percepts, max_height, step, time_left):
        # Joue un coup en utilisant la recherche Alpha-Beta.
        b = Board(percepts, max_height)
        return games.alphabeta_search((1, b), AvalamGame(),
                                      cutoff_test=self.cutoff_test, eval_fn=self.eval_fn)

if __name__ == "__main__":
    def options_cb(player, parser):
        # Ajoute une option pour définir la profondeur de recherche.
        parser.add_option("-d", "--depth", type="int", dest="depth",
                          default=-1, help="Définir la profondeur de recherche (par défaut : infinie)")

    def setup_cb(player, parser, options):
        # Configure le joueur en fonction des options fournies.
        if options.depth >= 0:
            player.depth = options.depth

    # Lancement principal du joueur Alpha-Beta.
    player_main(AlphaBetaPlayer(), options_cb, setup_cb)
