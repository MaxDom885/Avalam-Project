
from common import InvalidAction, Player, serve_player, player_main

class Board:
    """Représentation d'un plateau Avalam.
    self.m est un tableau bi-dimensionnel (self.rows par self.columns) représentant le plateau.
    La valeur absolue d'une cellule indique la hauteur de la tour. Le signe indique la couleur du sommet (négatif pour red, positif pour yellow).
    """
    max_height = 5  # Hauteur maximale des tours
    initial_board = [  # Plateau initial
        [0, 0, 1, -1, 0, 0, 0, 0, 0],
        [0, 1, -1, 1, -1, 0, 0, 0, 0],
        [0, -1, 1, -1, 1, -1, 1, 0, 0],
        [0, 1, -1, 1, -1, 1, -1, 1, -1],
        [1, -1, 1, -1, 0, -1, 1, -1, 1],
        [-1, 1, -1, 1, -1, 1, -1, 1, 0],
        [0, 0, 1, -1, 1, -1, 1, -1, 0],
        [0, 0, 0, 0, -1, 1, -1, 1, 0],
        [0, 0, 0, 0, 0, -1, 1, 0, 0]
    ]

    def __init__(self, percepts=initial_board, max_height=max_height, invert=False):
        """Initialise le plateau.
        Arguments :
        - percepts : matrice représentant le plateau
        - invert : inverser le signe des valeurs pour changer de joueur
        - max_height : hauteur maximale d'une tour
        """
        self.m = percepts
        self.rows = len(self.m)
        self.columns = len(self.m[0])
        self.max_height = max_height
        self.m = self.get_percepts(invert)  # Crée une copie des percepts

    def __str__(self):
        """Retourne une représentation en chaîne du plateau, adaptée en français."""
        def str_cell(i, j):
            x = self.m[i][j]
            if x:
                return f"{x:+2d}"  # Affiche les nombres avec un signe
            else:
                return " ."

        return "\n".join(" ".join(str_cell(i, j) for j in range(self.columns)) for i in range(self.rows))

    def clone(self):
        """Retourne une copie du plateau."""
        return Board(self.m)

    def get_percepts(self, invert=False):
        """Retourne les percepts correspondant à l'état actuel.
        Si invert est vrai, les signes des valeurs sont inversés.
        """
        mul = -1 if invert else 1
        return [[mul * self.m[i][j] for j in range(self.columns)] for i in range(self.rows)]

    def get_towers(self):
        """Génère toutes les tours sous forme de triplets (i, j, h) :
        - i : numéro de la ligne
        - j : numéro de la colonne
        - h : hauteur et propriétaire (signe)
        """
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j]:
                    yield (i, j, self.m[i][j])

    def is_action_valid(self, action):
        """Vérifie si une action est valide."""
        try:
            i1, j1, i2, j2 = action
            if i1 < 0 or j1 < 0 or i2 < 0 or j2 < 0 or i1 >= self.rows or j1 >= self.columns or i2 >= self.rows or j2 >= self.columns or (i1 == i2 and j1 == j2) or (abs(i1 - i2) > 1) or (abs(j1 - j2) > 1):
                return False
            h1 = abs(self.m[i1][j1])
            h2 = abs(self.m[i2][j2])
            if h1 <= 0 or h1 >= self.max_height or h2 <= 0 or h2 >= self.max_height or h1 + h2 > self.max_height:
                return False
            return True
        except (TypeError, ValueError):
            return False

    def get_tower_actions(self, i, j):
        """Génère toutes les actions possibles en déplaçant la tour (i, j)."""
        h = abs(self.m[i][j])
        if 0 < h < self.max_height:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    action = (i, j, i + di, j + dj)
                    if self.is_action_valid(action):
                        yield action

    def is_tower_movable(self, i, j):
        """Vérifie si la tour (i, j) peut être déplacée."""
        for action in self.get_tower_actions(i, j):
            return True
        return False

    def get_actions(self):
        """Génère toutes les actions valides sur ce plateau."""
        for i, j, h in self.get_towers():
            for action in self.get_tower_actions(i, j):
                yield action

    def play_action(self, action):
        """Exécute une action valide.
        Si l'action est invalide, lève une exception InvalidAction.
        Retourne le plateau mis à jour.
        """
        if not self.is_action_valid(action):
            raise InvalidAction(action)
        i1, j1, i2, j2 = action
        h1 = abs(self.m[i1][j1])
        h2 = abs(self.m[i2][j2])
        if self.m[i1][j1] < 0:
            self.m[i2][j2] = -(h1 + h2)
        else:
            self.m[i2][j2] = h1 + h2
        self.m[i1][j1] = 0
        return self

    def is_finished(self):
        """Retourne vrai si aucune action n'est possible (fin de partie)."""
        for action in self.get_actions():
            return False
        return True

    def get_winner(self):
        """Retourne un score indiquant le gagnant :
        - Score > 0 : joueur yellow gagne
        - Score < 0 : joueur red gagne
        - Score = 0 : match nul
        """
        score = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.m[i][j] < 0:
                    score -= 1
                elif self.m[i][j] > 0:
                    score += 1
        if score == 0:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.m[i][j] == -self.max_height:
                        score -= 1
                    elif self.m[i][j] == self.max_height:
                        score += 1
        return score

    def load_percepts(filename):
        """Charge un plateau à partir d'un fichier CSV."""
        with open(filename, "r") as f:
            import csv
            percepts = []
            for row in csv.reader(f):
                if not row:
                    continue
                row = [int(c.strip()) for c in row]
                if percepts:
                    assert len(row) == len(percepts[0]), "Toutes les lignes doivent avoir la même longueur"
                percepts.append(row)
        return percepts
