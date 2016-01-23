from abc import ABCMeta, abstractmethod


class AbstractGameTree(metaclass=ABCMeta):
    @abstractmethod
    def terminal(self):
        '''Return whether or not this state is terminal.'''
        pass

    @abstractmethod
    def utility(self, player):
        '''Return player's utility (between 0.0 and 100.0) for this state.'''
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

    @abstractmethod
    def __hash__(self):
        '''Hash the state to support memoization.'''
        pass
