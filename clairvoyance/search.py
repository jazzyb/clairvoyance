def minimax(self, state, players, depth=-1, return_scores=False):
    '''Run a minimax search on the current game state.

    This algorithm supports N-players with the following assumptions:
    * Players will make the move with the best utility for themselves.
    * Players do NOT move simultaneously.

    Arguments:
    state -- an AbstractGameTree
    players -- a list of all the players
    depth -- the distance in the tree to search (default=-1)
    return_scores -- if True, then return the best scores rather than the
        best move

    Return the best move for players[0].
    '''
    if depth == 0 or self.terminal():
        return state.heuristics()

    player = players.pop(0)
    players.append(player)
    best_scores = best_move = None
    for move in state.moves():
        scores = minimax(state.next(move), players, depth - 1, True)
        if best_scores is None or scores[player] > best_scores[player]:
            best, best_move = scores, move
    return best_scores if return_scores else best_move[player]
