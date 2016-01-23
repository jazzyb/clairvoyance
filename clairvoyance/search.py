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
        return state.heuristic(maxplayer)

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
    return best_score if return_score else best_move[player]


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
        return state.heuristic(player)

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
    return best_score if return_score else best_move[player]
