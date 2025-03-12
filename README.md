# **Gomoku-AI**

**Gomoku-AI** est une intelligence artificielle pour le jeu de Gomoku, implémentant l'algorithme **Minimax** avec élagage **Alpha-Beta** et des heuristiques optimisées. Ce projet permet de jouer contre une IA avec une prise de décision rapide et stratégique.


## **Fonctionnalités**

- **Algorithme Minimax avec élagage Alpha-Beta** : L'IA anticipe les coups adverses et maximise ses chances de victoire.
- **Heuristiques optimisées** : Des règles personnalisées évaluent les positions et améliorent les performances de l’IA.
- **Détection de patterns critiques** : L'IA détecte et bloque les configurations gagnantes de l'adversaire.
- **Interface en mode texte** : Une interface simple permet de suivre les parties.



## **Prérequis**

- **Python 3.8** ou version ultérieure.
- **Modules Python** :
  - `numpy` pour la gestion de la grille de jeu.

Pour installer les dépendances :
```bash
pip install numpy
```

---

## **Utilisation**

1. **Lancement du jeu** : Exécutez le script `gomoku_ai.py` pour démarrer une partie.
2. **Jouer une partie** : Suivez les instructions à l'écran pour placer vos pions.
   - Entrez votre coup sous la forme `row,column` (exemple : `7,7`).
3. **Tour de l'IA** : L'IA jouera automatiquement après votre coup.
4. **Fin de partie** : La partie se termine lorsqu'un joueur aligne 5 pions ou que la grille est pleine.

---

## **Structure du code**

### **Fonctions principales** :
- **`initialize_board(size=15)`** : Initialise une grille de jeu vide.
- **`generate_monomials(size=15, length=5)`** : Génère toutes les configurations possibles de 5 pions alignés (monômes).
- **`evaluate_monomials(board, player)`** : Évalue les scores des monômes pour un joueur donné.
- **`detect_critical_patterns(board, player)`** : Détecte les configurations critiques à bloquer.
- **`minimax(board, depth, alpha, beta, maximizing_player, player)`** : Implémente l'algorithme Minimax avec élagage Alpha-Beta.
- **`choose_best_move(board, player)`** : Choisit le meilleur coup pour l'IA.
- **`play_move(move, board, player)`** : Applique un coup sur la grille.
- **`terminal_test(board)`** : Vérifie si la partie est terminée (victoire ou grille pleine).

### **Fonctions d'affichage** :
- **`display(board)`** : Affiche la grille de jeu en mode texte.

---
