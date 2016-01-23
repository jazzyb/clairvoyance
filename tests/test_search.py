import unittest
from clairvoyance.game_tree import AbstractGameTree
from clairvoyance.search import minimax
from gdl import StateMachine

class GDLGameTree(AbstractGameTree):
    def __init__(self, players, kiffile=None):
        if kiffile:
            self.fsm = StateMachine()
            with open(kiffile, 'r') as f:
                self.fsm.store(file=f)
        self.players = players

    def terminal(self):
        return self.fsm.is_terminal()

    def heuristics(self):
        return self.fsm.score()

    def moves(self):
        moves = self.fsm.legal()
        current = self.players[0]
        ret = [{current: move} for move in moves[current]]
        for player in self.players:
            if player == current:
                continue
            for d in ret:
                # assume that only the current player has non-noop moves
                move_list = moves[player]
                assert len(move_list) == 1
                noop = move_list[0]
                assert noop == 'noop'
                d[player] = noop
        return ret

    def next(self, move):
        next = GDLGameTree(self.players[1:] + [self.players[0]])
        for player in move:
            self.fsm.move(player, move[player])
        next.fsm = self.fsm.next()
        return next

    def update(self, move):
        for player in move:
            self.fsm.move(player, move[player])
        self.fsm = self.fsm.next()

class TestMinimaxPuzzle(unittest.TestCase):
    def test_minimax(self):
        players = ['player']
        state = GDLGameTree(players, 'puzzles/8-puzzle.kif')
        self.assertEqual('(move 1 2)', minimax(state, players))
        state.update({'player': '(move 1 2)'})
        self.assertEqual('(move 2 2)', minimax(state, players))
        state.update({'player': '(move 2 2)'})
        self.assertEqual('(move 2 3)', minimax(state, players))
        state.update({'player': '(move 2 3)'})
        self.assertEqual('(move 3 3)', minimax(state, players))
        state.update({'player': '(move 3 3)'})

        # verify the final state
        db = [str(x[0]) for x in state.fsm.db.facts[('true', 1)]]
        results = [
                '(step 4)',
                '(cell 1 1 1)',
                '(cell 1 2 2)',
                '(cell 1 3 3)',
                '(cell 2 1 4)',
                '(cell 2 2 5)',
                '(cell 2 3 6)',
                '(cell 3 1 7)',
                '(cell 3 2 8)',
                '(cell 3 3 b)',
        ]
        for i in results:
            self.assertIn(i, db)
