import copy
import numpy as np

# Initialisation de la grille Gomoku
def initialize_board(size=15):
    return np.zeros((size, size), dtype=int)

# Pré-génération des monomes pour toutes les configurations possibles
MONOMES = []
def generate_monomials(size=15, length=5):
    for i in range(size):
        for j in range(size):
            # Horizontal
            if j + length <= size:
                MONOMES.append([(i, j + k) for k in range(length)])
            # Vertical
            if i + length <= size:
                MONOMES.append([(i + k, j) for k in range(length)])
            # Diagonale \
            if i + length <= size and j + length <= size:
                MONOMES.append([(i + k, j + k) for k in range(length)])
            # Diagonale /
            if i + length <= size and j - length + 1 >= 0:
                MONOMES.append([(i + k, j - k) for k in range(length)])

# Génération des monomes
generate_monomials()

# Ajout du pattern spécifique pour le blocage
PATTERNS = {
    "win": [
        [1, 1, 1, 1, 1],  # Winning pattern
    ],
    "block_critical": [
        [0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0],
    ]
}

# Fonction pour vérifier si un monome est actif
def is_monomial_active(board, monome, player):
    return all(board[x, y] in [0, player] for x, y in monome)

# Fonction pour évaluer les scores des monomes
def evaluate_monomials(board, player):
    scores = {}
    for monome in MONOMES:
        if is_monomial_active(board, monome, player):
            score = sum(1 if board[x, y] == player else 0 for x, y in monome)
            for x, y in monome:
                if board[x, y] == 0:
                    scores[(x, y)] = scores.get((x, y), 0) + score
    return scores

# Détection des patterns critiques spécifiques
def detect_critical_patterns(board, player):
    size = board.shape[0]
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal \, Diagonal /

    for x in range(size):
        for y in range(size):
            for dx, dy in directions:
                for pattern in PATTERNS["block_critical"]:
                    matched = True
                    for i in range(len(pattern)):
                        nx, ny = x + i * dx, y + i * dy
                        if 0 <= nx < size and 0 <= ny < size:
                            cell = board[nx, ny]
                            if pattern[i] == 1 and cell != player:
                                matched = False
                                break
                            elif pattern[i] == 0 and cell != 0:
                                matched = False
                                break
                        else:
                            matched = False
                            break
                    if matched:
                        # Retourne la première case vide pour bloquer
                        for i in range(len(pattern)):
                            nx, ny = x + i * dx, y + i * dy
                            if pattern[i] == 0 and board[nx, ny] == 0:
                                return (nx, ny)
    return None

# Fonction pour évaluer l'état du plateau (heuristique)
def evaluate_board(board, player):
    opponent = 3 - player
    player_scores = evaluate_monomials(board, player)
    opponent_scores = evaluate_monomials(board, opponent)

    player_total = sum(player_scores.values())
    opponent_total = sum(opponent_scores.values())

    # Donne un avantage aux alignements du joueur actif
    return player_total - opponent_total

# Minimax amélioré avec détection de patterns critiques
def minimax(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or terminal_test(board):
        return evaluate_board(board, player), None

    opponent = 3 - player
    best_move = None

    # Vérifie les patterns critiques
    critical_move = detect_critical_patterns(board, opponent if maximizing_player else player)
    if critical_move:
        return 1000 if maximizing_player else -1000, critical_move

    if maximizing_player:
        max_eval = float('-inf')
        for move in actions(board):
            new_board = play_move(move, copy.deepcopy(board), player)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, False, opponent)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in actions(board):
            new_board = play_move(move, copy.deepcopy(board), opponent)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, True, player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# Fonction pour choisir le meilleur coup
def choose_best_move(board, player):
    _, move = minimax(board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True, player=player)
    return move

# Fonction pour appliquer un coup
def play_move(move, board, player):
    x, y = move
    if board[x, y] != 0:
        raise ValueError("Invalid move: position already occupied.")
    board[x, y] = player
    return board

# Fonction pour tester si la partie est terminée
def terminal_test(board):
    for monome in MONOMES:
        values = [board[x, y] for x, y in monome]
        if all(v == 1 for v in values):
            print("Player 1 has won!")
            return True
        if all(v == 2 for v in values):
            print("Player 2 has won!")
            return True
    return False

# Fonction d'affichage
def display(board):
    symbols = {0: '.', 1: 'X', 2: 'O'}
    for row in board:
        print(" ".join(symbols[cell] for cell in row))
    print()

# Fonction pour obtenir les coups possibles
def actions(board):
    return [(i, j) for i in range(board.shape[0]) for j in range(board.shape[1]) if board[i, j] == 0]

# Initialisation
board = initialize_board()
print("Game started. Input your move as 'row,column' (e.g., 0,2).")
display(board)

# Boucle principale pour jouer
while not terminal_test(board):
    move = input("Your move (row,column): ")
    x, y = map(int, move.split(','))
    board = play_move((x, y), board, 1)
    display(board)

    if terminal_test(board):
        break

    ai_move = choose_best_move(board, 2)
    print(f"AI plays: {ai_move}")
    board = play_move(ai_move, board, 2)
    display(board)
