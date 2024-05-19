"""Test of figures module"""

import unittest
import sys
import os
sys.path.insert(1, os.path.dirname(__file__) + '/../client/src')
import figures


class TestCoordinatesTranslators(unittest.TestCase):

    def setUp(self):
        pass

    def test_coordinates_translators(self):
        self.assertEqual(figures.coordinates_to_computer('e2'), (4, 1))
        self.assertEqual(figures.coordinates_to_computer((4, 1)), (4, 1))

        self.assertEqual(figures.coordinates_to_human((4, 1)), 'e2')
        self.assertEqual(figures.coordinates_to_human('e2'), 'e2')

    def tearDown(self):
        pass


class TestKing(unittest.TestCase):

    def setUp(self):
        pass

    def test_King(self):
        figure = figures.King(4, 4, 'b')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'Kb')

        figure = figures.King(4, 4, 'w')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'Kw')

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure.get_possible_moves(board),
                         ['d4', 'd5', 'd6', 'e4', 'e6', 'f4', 'f5', 'f6'])

        board[3][4] = 'Pw'
        board[4][3] = 'Pw'
        board[5][4] = 'Pw'
        board[4][5] = 'Pw'
        self.assertEqual(figure.get_possible_moves(board),
                         ['d4', 'd6', 'f4', 'f6'])
        board[3][3] = 'Pw'
        board[5][3] = 'Pw'
        board[3][5] = 'Pw'
        board[5][5] = 'Pw'
        self.assertEqual(figure.get_possible_moves(board), [])

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure.get_possible_moves(board),
                         ['d4', 'd5', 'd6', 'e4', 'e6', 'f4', 'f5', 'f6'])

        board[3][4] = 'Pb'
        board[4][3] = 'Pb'
        board[5][4] = 'Pb'
        board[4][5] = 'Pb'
        self.assertEqual(figure.get_possible_moves(board),
                         ['d4', 'd5', 'd6', 'e4', 'e6', 'f4', 'f5', 'f6'])
        board[3][3] = 'Pb'
        board[5][3] = 'Pb'
        board[3][5] = 'Pb'
        board[5][5] = 'Pb'
        self.assertEqual(figure.get_possible_moves(board),
                         ['d4', 'd5', 'd6', 'e4', 'e6', 'f4', 'f5', 'f6'])

        figure1 = figures.King(4, 0, 'w')
        figure2 = figures.King(4, 7, 'b')
        board = [[' ' for i in range(8)] for j in range(8)]
        board[0][0] = 'Rw'
        board[7][0] = 'Rw'
        board[0][7] = 'Rb'
        board[7][7] = 'Rb'
        self.assertEqual(figure1.get_possible_moves(board),
                         ['c1', 'd1', 'd2', 'e2', 'f1', 'f2', 'g1'])
        self.assertEqual(figure2.get_possible_moves(board),
                         ['c8', 'd7', 'd8', 'e7', 'f7', 'f8', 'g8'])

        figure = figures.King(4, 0, 'w')
        board = [[' ' for i in range(8)] for j in range(8)]
        board[0][0] = 'Rw'
        board[1][0] = 'Knw'
        board[7][0] = 'Rb'
        self.assertEqual(figure.get_possible_moves(board),
                         ['d1', 'd2', 'e2', 'f1', 'f2'])
        board[6][0] = 'Knb'
        figure.update_possible_moves(board)
        self.assertEqual(figure.possible_moves,
                         [(3, 0), (3, 1), (4, 1), (5, 0), (5, 1)])

    def tearDown(self):
        pass


class TestQueen(unittest.TestCase):

    def setUp(self):
        pass

    def test_Queen(self):
        figure = figures.Queen(4, 4, 'b')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'Qb')

        figure = figures.Queen(4, 4, 'w')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'Qw')

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure.get_possible_moves(board),
                         ['a1', 'a5', 'b2', 'b5', 'b8', 'c3', 'c5', 'c7', 'd4',
                          'd5', 'd6', 'e1', 'e2', 'e3', 'e4', 'e6', 'e7', 'e8',
                          'f4', 'f5', 'f6', 'g3', 'g5', 'g7', 'h2', 'h5', 'h8'])

        board[2][4] = 'Pw'
        board[4][2] = 'Pw'
        board[6][4] = 'Pw'
        board[4][6] = 'Pw'
        self.assertEqual(figure.get_possible_moves(board),
                         ['a1', 'b2', 'b8', 'c3', 'c7', 'd4', 'd5', 'd6',
                          'e4', 'e6', 'f4', 'f5', 'f6', 'g3', 'g7', 'h2', 'h8'])
        board[2][2] = 'Pw'
        board[6][2] = 'Pw'
        board[2][6] = 'Pw'
        board[6][6] = 'Pw'
        self.assertEqual(figure.get_possible_moves(board),
                         ['d4', 'd5', 'd6', 'e4', 'e6', 'f4', 'f5', 'f6'])

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure.get_possible_moves(board),
                         ['a1', 'a5', 'b2', 'b5', 'b8', 'c3', 'c5',
                          'c7', 'd4', 'd5', 'd6', 'e1', 'e2', 'e3',
                          'e4', 'e6', 'e7', 'e8', 'f4', 'f5', 'f6',
                          'g3', 'g5', 'g7', 'h2', 'h5', 'h8'])

        board[2][4] = 'Pb'
        board[4][2] = 'Pb'
        board[6][4] = 'Pb'
        board[4][6] = 'Pb'
        self.assertEqual(figure.get_possible_moves(board),
                         ['a1', 'b2', 'b8', 'c3', 'c5', 'c7', 'd4',
                          'd5', 'd6', 'e3', 'e4', 'e6', 'e7', 'f4',
                          'f5', 'f6', 'g3', 'g5', 'g7', 'h2', 'h8'])
        board[2][2] = 'Pb'
        board[6][2] = 'Pb'
        board[2][6] = 'Pb'
        board[6][6] = 'Pb'
        figure.update_possible_moves(board)
        self.assertEqual(figure.possible_moves,
                         [(2, 2), (2, 4), (2, 6), (3, 3), (3, 4),
                          (3, 5), (4, 2), (4, 3), (4, 5), (4, 6),
                          (5, 3), (5, 4), (5, 5), (6, 2), (6, 4), (6, 6)])

    def tearDown(self):
        pass


class TestRook(unittest.TestCase):

    def setUp(self):
        pass

    def test_Rook(self):
        figure = figures.Rook(4, 4, 'b')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'Rb')

        figure = figures.Rook(4, 4, 'w')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'Rw')

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure.get_possible_moves(board),
                         ['a5', 'b5', 'c5', 'd5', 'e1', 'e2', 'e3',
                          'e4', 'e6', 'e7', 'e8', 'f5', 'g5', 'h5'])

        board[2][4] = 'Pw'
        board[4][2] = 'Pw'
        board[6][4] = 'Pw'
        board[4][6] = 'Pw'
        self.assertEqual(figure.get_possible_moves(board),
                         ['d5', 'e4', 'e6', 'f5'])

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure.get_possible_moves(board),
                         ['a5', 'b5', 'c5', 'd5', 'e1', 'e2', 'e3',
                          'e4', 'e6', 'e7', 'e8', 'f5', 'g5', 'h5'])

        board[2][4] = 'Pb'
        board[4][2] = 'Pb'
        board[6][4] = 'Pb'
        board[4][6] = 'Pb'

        figure.update_possible_moves(board)
        self.assertEqual(figure.possible_moves,
                         [(2, 4), (3, 4), (4, 2), (4, 3),
                          (4, 5), (4, 6), (5, 4), (6, 4)])

    def tearDown(self):
        pass


class TestKnight(unittest.TestCase):

    def setUp(self):
        pass

    def test_Knight(self):
        figure = figures.Knight(4, 4, 'b')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'KNb')

        figure = figures.Knight(4, 4, 'w')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'KNw')

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure.get_possible_moves(board),
                         ['c4', 'c6', 'd3', 'd7', 'f3', 'f7', 'g4', 'g6'])

        board[2][3] = 'Pw'
        board[2][5] = 'Pw'
        board[6][3] = 'Pb'
        board[6][5] = 'Pb'
        figure.update_possible_moves(board)
        self.assertEqual(figure.possible_moves,
                         [(3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)])

    def tearDown(self):
        pass


class TestBishop(unittest.TestCase):

    def setUp(self):
        pass

    def test_Bishop(self):
        figure = figures.Bishop(4, 4, 'b')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'Bb')

        figure = figures.Bishop(4, 4, 'w')
        self.assertEqual(figure.x, 4)
        self.assertEqual(figure.y, 4)
        self.assertEqual(figure.label, 'Bw')

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure.get_possible_moves(board),
                         ['a1', 'b2', 'b8', 'c3', 'c7', 'd4',
                          'd6', 'f4', 'f6', 'g3', 'g7', 'h2', 'h8'])

        board[2][2] = 'Pw'
        board[2][6] = 'Pw'
        board[6][2] = 'Pb'
        board[6][6] = 'Pb'
        figure.update_possible_moves(board)
        self.assertEqual(figure.possible_moves,
                         [(3, 3), (3, 5), (5, 3), (5, 5), (6, 2), (6, 6)])

    def tearDown(self):
        pass


class TestPawn(unittest.TestCase):

    def setUp(self):
        pass

    def test_Pawn(self):
        figure1 = figures.Pawn(4, 4, 'w')
        self.assertEqual(figure1.x, 4)
        self.assertEqual(figure1.y, 4)
        self.assertEqual(figure1.label, 'Pw')

        figure2 = figures.Pawn(4, 4, 'b')
        self.assertEqual(figure2.x, 4)
        self.assertEqual(figure2.y, 4)
        self.assertEqual(figure2.label, 'Pb')

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure1.get_possible_moves(board), ['e6'])
        self.assertEqual(figure2.get_possible_moves(board), ['e4'])

        figure1 = figures.Pawn(4, 1, 'w')
        figure2 = figures.Pawn(4, 6, 'b')

        board = [[' ' for i in range(8)] for j in range(8)]
        self.assertEqual(figure1.get_possible_moves(board), ['e3', 'e4'])
        self.assertEqual(figure2.get_possible_moves(board), ['e5', 'e6'])

        board[3][2] = 'Pb'
        board[5][2] = 'Pb'
        board[3][5] = 'Pw'
        board[5][5] = 'Pw'
        figure1.update_possible_moves(board)
        self.assertEqual(figure1.possible_moves,
                         [(3, 2), (4, 2), (4, 3), (5, 2)])
        figure2.update_possible_moves(board)
        self.assertEqual(figure2.possible_moves,
                         [(3, 5), (4, 4), (4, 5), (5, 5)])

        figure1 = figures.Pawn(4, 4, 'w')
        board = [[' ' for i in range(8)] for j in range(8)]
        board[3][4] = 'Pb'
        board[5][4] = 'Pb'
        self.assertEqual(figure1.get_possible_moves(board), ['d6', 'e6', 'f6'])

        figure2 = figures.Pawn(4, 3, 'b')
        board = [[' ' for i in range(8)] for j in range(8)]
        board[3][3] = 'Pw'
        board[5][3] = 'Pw'
        self.assertEqual(figure2.get_possible_moves(board), ['d3', 'e3', 'f3'])

    def tearDown(self):
        pass
