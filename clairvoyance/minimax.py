from abc import ABCMeta, abstractmethod


class MinimaxSearchTree(metaclass=ABCMeta):
    @abstractmethod
    def terminal(self):
        '''Return whether or not this state is terminal.'''
        pass

    @abstractmethod
    def heuristics(self):
        '''Return a heuristic (between 0.0 and 100.0) for each player for the
        current state.  Return value is a dict of {player: score}.
        '''
        pass

    @abstractmethod
    def moves(self):
        '''Return all legal moves for this state for all players.  Return
        value is a list of dicts:
            [{player1: move, player2: move, ...}, {player1: move, ...}, ...]
        '''
        pass

    @abstractmethod
    def next(self, move):
        '''Updates the game state.  Argument move is an item from the return
        value of moves().  Return a copy of the next state.
        '''
        pass

#    TODO:  For memoization later.
#    @abstractmethod
#    def __hash__(self):
#        pass

    def search(self, players, depth=-1, return_scores=False):
        '''Run a minimax search on the current game state.

        This algorithm supports N-players with the following assumptions:
        * Players will make the move with the best utility for themselves.
        * Players do NOT move simultaneously.

        Arguments:
        players -- a list of all the players
        depth -- the distance in the tree to search (default=-1)
        return_scores -- if True, then return the best scores rather than the
            best move

        Return the best move for players[0].
        '''
        if depth == 0 or self.terminal():
            return self.heuristics()

        player = players.pop(0)
        players.append(player)
        best_scores = best_move = None
        for move in self.moves():
            scores = self.next(move).search(players, depth - 1, True)
            if best_scores is None or scores[player] > best_scores[player]:
                best, best_move = scores, move
        return best_scores if return_scores else best_move[player]
