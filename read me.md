# Projet Avalam

Ce projet implémente le jeu Avalam, un jeu de stratégie où deux joueurs s'affrontent sur un plateau en déplaçant et en empilant des tours de jetons de différentes hauteurs. Le projet inclut également une implémentation du jeu de morpion (Tic-Tac-Toe) utilisant l'algorithme MiniMax avec une interface graphique.

## Structure du Projet

Le projet est organisé en plusieurs fichiers :

- `avalam.py` : Contient la logique du jeu Avalam, y compris la représentation du plateau et les règles du jeu.
- `alphabeta_player.py` : Implémente un agent utilisant l'algorithme Alpha-Beta pour jouer à Avalam.
- `player.py` : Contient l'implémentation de votre agent personnalisé pour le concours.
- `random_player.py` : Implémente un joueur aléatoire pour tester le jeu.
- `game.py` : Gère le déroulement du jeu Avalam, y compris la gestion des joueurs et l'interface utilisateur.
- `gui.py` : Fournit une interface graphique pour le jeu de morpion (Tic-Tac-Toe).
- `tictactoe.py` : Contient la logique du jeu de morpion.
- `minimax_player.py` : Implémente un agent utilisant l'algorithme MiniMax pour jouer au morpion.
- `game_runner.py` : Contient la logique pour exécuter le jeu de morpion et permettre aux joueurs de jouer contre l'agent MiniMax.

## Auteurs

- ATTOH James
- BIAOU Marius
- HOUESSOU Kenyy
- YACOUBOU Masmoud


## Prérequis

- Python 3.9 ou supérieur
- Bibliothèque `tkinter` pour l'interface graphique

## Installation

1. **Installer Python 3.9 ou supérieur** : Assurez-vous d'avoir Python 3.9 ou une version ultérieure installée sur votre machine. Vous pouvez vérifier votre version de Python avec la commande suivante :
    ```sh
    python --version
    ```

2. **Installer les dépendances** : Vous aurez besoin de quelques bibliothèques Python. Vous pouvez les installer via `pip` :
    ```sh
    pip install xmlrpcserver
    ```

## Lancer le Jeu Avalam

### Lancer le Jeu avec Deux Joueurs Humains

```sh
python game.py human human
```
### Lancer le Jeu avec un Joueur Humain et un Joueur Aléatoire
Dans un terminal :
```sh
python random_player.py -p 8000
```
Dans un autre terminal :
```sh
python game.py human http://localhost:8000
```
### Lancer le Jeu avec un Joueur Humain et un Agent IA (Alpha-Beta)
Dans un terminal :
```sh
python alphabeta_player.py -p 8000
```
### Dans un autre terminal :
```sh
python game.py human http://localhost:8000
```
### Lancer le Jeu avec un Joueur Humain et Votre Agent Personnalisé
Dans un terminal :
```sh
python player.py -p 8000
```
### Dans un autre terminal :
```sh
python game.py human http://localhost:8000
```
### Lancer le Jeu de Morpion avec l'Interface Graphique
Pour utiliser l'interface graphique, assurez-vous d'avoir les bindings Tk pour Python installés. Sur les systèmes basés sur Debian, vous pouvez installer le paquet python3-tk :
```sh
sudo apt-get install python3-tk
```
Ensuite, lancez le jeu avec l'interface graphique :
```sh
python gui.py
```
### Commandes Avancées
Enregistrer une Partie
```sh
python game.py human human -w trace.pkl
```
### Rejouer une Partie Enregistrée
```sh
python game.py -r trace.pkl
```
### Définir un Temps de Crédit par Joueur
```sh
python game.py human human -t 60
```
### Inverser le Plateau Initial
```sh
python game.py human human --invert
```
### Définir la Hauteur Maximale des Tours
```sh
python game.py human human --tower-height 6
```
### Charger un Plateau Initial Personnalisé
```sh
python game.py human human --board custom_board.csv
```
### Désactiver l'Interface Graphique
```sh
python game.py human human --no-gui
```
### Lancer le Jeu en Mode Headless (sans Interface Utilisateur)
```sh
python game.py human human --headless
```
### Activer le Mode Verbose
```sh
python game.py human human -v
```