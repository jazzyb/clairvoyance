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
