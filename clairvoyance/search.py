import random
from clairvoyance.memoization import memoize


@memoize
def minimax(state, players, depth=-1, return_score=False, maxplayer=None):
    '''Run a minimax search on the current game state.

    This algorithm supports N-players with the following assumptions:
    * Opponents will make the move with the worst utility for maxplayer.
    * Players do NOT move simultaneously.

    Arguments:
    state -- an AbstractGameTree
    players -- a list of all the players
    depth -- the distance in the tree to search (default=-1)
    return_score -- if True, then return the best score instead of the best move
    maxplayer -- the player whose score is being maximized for

    Return the best move for maxplayer.
    '''
    maxplayer = maxplayer or players[0]
    if depth == 0 or state.terminal():
        return state.utility(maxplayer)

    player = players[0]
    players = players[1:] + [player]
    best_move = None
    if player == maxplayer:
        best_score = 0.0
        for move in state.moves():
            score = minimax(state.next(move), players, depth - 1, True, maxplayer)
            if score > best_score:
                best_score, best_move = score, move
    else:
        best_score = 100.0
        for move in state.moves():
            score = minimax(state.next(move), players, depth - 1, True, maxplayer)
            if score < best_score:
                best_score, best_move = score, move
    if return_score:
        return best_score
    if best_move:
        return best_move[player]
    return state.moves()[0][player]


@memoize
def alphabeta(state, player, depth=-1, return_score=False,
        maximize_player=True, alpha=0.0, beta=100.0):
    '''Run a minimax search on the current game state with alpha-beta pruning.

    This algorithm only supports EXACTLY 2 players.

    Arguments:
    state -- an AbstractGameTree
    player -- the maximizing player
    depth -- the distance in the tree to search (default=-1)
    return_score -- if True, then return the best score instead of the best
        move (default=False)
    maximize_player -- True if maximizing for the current player (default=True)
    alpha -- the alpha cut-off (default=-INFINITY)
    beta -- the beta cut-off (default=+INFINITY)

    Return the best move for player.
    '''
    if depth == 0 or state.terminal():
        return state.utility(player)

    best_move = None
    if maximize_player:
        best_score = 0.0
        for move in state.moves():
            score = alphabeta(state.next(move), player, depth - 1, True, False, alpha, beta)
            if score > best_score:
                best_score, best_move = score, move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
    else:
        best_score = 100.0
        for move in state.moves():
            score = alphabeta(state.next(move), player, depth - 1, True, True, alpha, beta)
            if score < best_score:
                best_score, best_move = score, move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
    if return_score:
        return best_score
    if best_move:
        return best_move[player]
    return state.moves()[0][player]


def montecarlo(state, player, probes=1):
    '''Run a Monte Carlo search on the current game state.

    Arguments:
    state -- an AbstractGameTree
    player -- player to calculate utility for
    probes -- number of paths to average the utility over

    Return the estimated utility of the state averaged over the probes.
    '''
    if state.terminal():
        return state.utility(player)

    total = 0
    moves = state.moves()
    for _ in range(probes):
        total += montecarlo(state.next(random.choice(moves)), player)
    return total / probes
