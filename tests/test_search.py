import unittest
from clairvoyance.game_tree import AbstractGameTree
from clairvoyance.search import alphabeta, minimax
from gdl import StateMachine


class GDLGameTree(AbstractGameTree):
    def __init__(self, kiffile, players, fsm=None):
        self.kiffile = kiffile
        self.players = players
        self.fsm = fsm

    def start(self):
        if self.fsm is None:
            self.fsm = StateMachine()
            with open(self.kiffile, 'r') as f:
                self.fsm.store(file=f)

    def terminal(self):
        return self.fsm.is_terminal()

    def heuristic(self, player):
        return float(self.fsm.score(player))

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
        next = GDLGameTree(self.kiffile, self.players, self.fsm)
        next.update(move)
        return next

    def update(self, move):
        for player in move:
            self.fsm.move(player, move[player])
        self.fsm = self.fsm.next()
        self.players = self.players[1:] + [self.players[0]]

    def __hash__(self):
        return hash(self.kiffile) ^ hash(self.fsm)

class TestMinimaxPuzzle(unittest.TestCase):
    def test_solo_puzzle(self):
        players = ['player']
        state = GDLGameTree('puzzles/8-puzzle.kif', players)
        state.start()
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

class TestMinimaxGame(unittest.TestCase):
    def test_oplayer_tic_tac_toe(self):
        players = ['oplayer', 'xplayer']
        state = GDLGameTree('games/tic-tac-toe.kif', players[::-1])
        state.start()
        state.update({'xplayer': '(mark 2 2)', 'oplayer': 'noop'})
        move = minimax(state, players)
        self.assertNotIn(move, ('(mark 1 2)', '(mark 2 1)', '(mark 2 3)', '(mark 3 2)'))
        state.update({'oplayer': '(mark 1 1)', 'xplayer': 'noop'})
        state.update({'xplayer': '(mark 2 1)', 'oplayer': 'noop'})
        state.update({'oplayer': '(mark 2 3)', 'xplayer': 'noop'})
        state.update({'xplayer': '(mark 3 1)', 'oplayer': 'noop'})
        self.assertEqual('(mark 1 3)', minimax(state, players))
        self.assertEqual(100.0, minimax(state, players, -1, True))

class TestAlphabetaGame(unittest.TestCase):
    def test_oplayer_tic_tac_toe(self):
        players = ['oplayer', 'xplayer']
        state = GDLGameTree('games/tic-tac-toe.kif', players[::-1])
        state.start()
        state.update({'xplayer': '(mark 2 2)', 'oplayer': 'noop'})
        move = alphabeta(state, players[0])
        self.assertNotIn(move, ('(mark 1 2)', '(mark 2 1)', '(mark 2 3)', '(mark 3 2)'))
        state.update({'oplayer': '(mark 1 1)', 'xplayer': 'noop'})
        state.update({'xplayer': '(mark 2 1)', 'oplayer': 'noop'})
        state.update({'oplayer': '(mark 2 3)', 'xplayer': 'noop'})
        state.update({'xplayer': '(mark 3 1)', 'oplayer': 'noop'})
        self.assertEqual('(mark 1 3)', alphabeta(state, players[0]))
        self.assertEqual(100.0, alphabeta(state, players[0], -1, True))
