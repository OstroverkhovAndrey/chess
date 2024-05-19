"""Test of chess_game module"""

import unittest
import sys
import os
sys.path.insert(1, os.path.dirname(__file__) + '/../client/src')
from chess_game import Game


class TestGameBeginning(unittest.TestCase):

    def setUp(self):
        pass

    def test_game_beginning(self):
        game = Game("w")
        self.assertEqual(game.get_possible_moves(), {'a1': [],
                                                     'a2': ['a3', 'a4'],
                                                     'b1': ['a3', 'c3'],
                                                     'b2': ['b3', 'b4'],
                                                     'c1': [],
                                                     'c2': ['c3', 'c4'],
                                                     'd1': [],
                                                     'd2': ['d3', 'd4'],
                                                     'e1': [],
                                                     'e2': ['e3', 'e4'],
                                                     'f1': [],
                                                     'f2': ['f3', 'f4'],
                                                     'g1': ['f3', 'h3'],
                                                     'g2': ['g3', 'g4'],
                                                     'h1': [],
                                                     'h2': ['h3', 'h4']})

        self.assertTrue(game.isMyMove())
        self.assertFalse(game.isDrawMove("e2", "e4"))
        self.assertFalse(game.isWinMove("e2", "e4"))
        self.assertTrue(game.isPossibleMove("e2", "e4"))
        game.move("e2", "e4")

        self.assertFalse(game.isMyMove())
        game.move_from_server("e7", "e5")

        self.assertTrue(game.isMyMove())
        self.assertEqual(game.get_possible_moves()["e4"], [])

    def tearDown(self):
        pass


class TestGetBoard(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_board(self):
        game = Game("w")

        self.assertEqual(game.get_board(), '\n   a    b    c    d    e    f    g    h\n ┌────┬────┬────┬────┬────┬────┬────┬────┐\n8│ Rb │KNb │ Bb │ Qb │ Kb │ Bb │KNb │ Rb │8\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n7│ Pb │ Pb │ Pb │ Pb │ Pb │ Pb │ Pb │ Pb │7\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n6│    │    │    │    │    │    │    │    │6\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n5│    │    │    │    │    │    │    │    │5\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n4│    │    │    │    │    │    │    │    │4\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n3│    │    │    │    │    │    │    │    │3\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n2│ Pw │ Pw │ Pw │ Pw │ Pw │ Pw │ Pw │ Pw │2\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n1│ Rw │KNw │ Bw │ Qw │ Kw │ Bw │KNw │ Rw │1\n └────┴────┴────┴────┴────┴────┴────┴────┘\n   a    b    c    d    e    f    g    h\n')

        self.assertTrue(game.isMyMove())
        self.assertFalse(game.isDrawMove("e2", "e4"))
        self.assertFalse(game.isWinMove("e2", "e4"))
        self.assertTrue(game.isPossibleMove("e2", "e4"))
        game.move("e2", "e4")

        self.assertEqual(game.get_board(), '\n   a    b    c    d    e    f    g    h\n ┌────┬────┬────┬────┬────┬────┬────┬────┐\n8│ Rb │KNb │ Bb │ Qb │ Kb │ Bb │KNb │ Rb │8\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n7│ Pb │ Pb │ Pb │ Pb │ Pb │ Pb │ Pb │ Pb │7\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n6│    │    │    │    │    │    │    │    │6\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n5│    │    │    │    │    │    │    │    │5\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n4│    │    │    │    │ Pw │    │    │    │4\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n3│    │    │    │    │    │    │    │    │3\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n2│ Pw │ Pw │ Pw │ Pw │    │ Pw │ Pw │ Pw │2\n ├────┼────┼────┼────┼────┼────┼────┼────┤\n1│ Rw │KNw │ Bw │ Qw │ Kw │ Bw │KNw │ Rw │1\n └────┴────┴────┴────┴────┴────┴────┴────┘\n   a    b    c    d    e    f    g    h\n')

    def tearDown(self):
        pass


class TestEat(unittest.TestCase):

    def setUp(self):
        pass

    def test_eat(self):
        game1 = Game("w")
        game2 = Game("b")

        self.assertFalse(game1.isDrawMove("e2", "e4"))
        self.assertFalse(game1.isWinMove("e2", "e4"))
        self.assertTrue(game1.isPossibleMove("e2", "e4"))
        game1.move("e2", "e4")
        game2.move_from_server("e2", "e4")

        self.assertFalse(game2.isDrawMove("d7", "d5"))
        self.assertFalse(game2.isWinMove("d7", "d5"))
        self.assertTrue(game2.isPossibleMove("d7", "d5"))
        game2.move("d7", "d5")
        game1.move_from_server("d7", "d5")

        self.assertFalse(game1.isDrawMove("e4", "d5"))
        self.assertFalse(game1.isWinMove("e4", "d5"))
        self.assertTrue(game1.isPossibleMove("e4", "d5"))
        game1.move("e4", "d5")
        game2.move_from_server("e4", "d5")

        self.assertEqual(game1.board, [['Rw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Rb'],
                                      ['KNw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'KNb'],
                                      ['Bw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Bb'],
                                      ['Qw', 'Pw', ' ', ' ', 'Pw', ' ', ' ', 'Qb'],
                                      ['Kw', ' ', ' ', ' ', ' ', ' ', 'Pb', 'Kb'],
                                      ['Bw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Bb'],
                                      ['KNw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'KNb'],
                                      ['Rw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Rb']])
#        self.assertEqual(len(game1.white_figures), 16)
#        self.assertEqual(len(game1.black_figures), 15)

    def tearDown(self):
        pass


class TestEnPassant(unittest.TestCase):

    def setUp(self):
        pass

    def test_en_passant(self):
        game1 = Game("w")
        game2 = Game("b")

        self.assertFalse(game1.isDrawMove("e2", "e4"))
        self.assertFalse(game1.isWinMove("e2", "e4"))
        self.assertTrue(game1.isPossibleMove("e2", "e4"))
        game1.move("e2", "e4")
        game2.move_from_server("e2", "e4")

        self.assertFalse(game2.isDrawMove("d7", "d5"))
        self.assertFalse(game2.isWinMove("d7", "d5"))
        self.assertTrue(game2.isPossibleMove("d7", "d5"))
        game2.move("d7", "d5")
        game1.move_from_server("d7", "d5")

        self.assertFalse(game1.isDrawMove("e4", "e5"))
        self.assertFalse(game1.isWinMove("e4", "e5"))
        self.assertTrue(game1.isPossibleMove("e4", "e5"))
        game1.move("e4", "e5")
        game2.move_from_server("e4", "e5")

        self.assertFalse(game2.isDrawMove("g7", "g5"))
        self.assertFalse(game2.isWinMove("g7", "g5"))
        self.assertTrue(game2.isPossibleMove("g7", "g5"))
        game2.move("g7", "g5")
        game1.move_from_server("g7", "g5")

        self.assertFalse(game1.isDrawMove("e5", "d6"))
        self.assertFalse(game1.isWinMove("e5", "d6"))
        self.assertTrue(game1.isPossibleMove("e5", "d6"))
        game1.move("e5", "d6")
        game2.move_from_server("e5", "d6")

        self.assertFalse(game2.isDrawMove("g5", "g4"))
        self.assertFalse(game2.isWinMove("g5", "g4"))
        self.assertTrue(game2.isPossibleMove("g5", "g4"))
        game2.move("g5", "g4")
        game1.move_from_server("g5", "g4")

        self.assertFalse(game1.isDrawMove("h2", "h4"))
        self.assertFalse(game1.isWinMove("h2", "h4"))
        self.assertTrue(game1.isPossibleMove("h2", "h4"))
        game1.move("h2", "h4")
        game2.move_from_server("h2", "h4")

        self.assertFalse(game2.isDrawMove("g4", "h3"))
        self.assertFalse(game2.isWinMove("g4", "h3"))
        self.assertTrue(game2.isPossibleMove("g4", "h3"))
        game2.move("g4", "h3")
        game1.move_from_server("g4", "h3")

        self.assertEqual(game1.board, [['Rw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Rb'],
                                      ['KNw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'KNb'],
                                      ['Bw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Bb'],
                                      ['Qw', 'Pw', ' ', ' ', ' ', 'Pw', ' ', 'Qb'],
                                      ['Kw', ' ', ' ', ' ', ' ', ' ', 'Pb', 'Kb'],
                                      ['Bw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Bb'],
                                      ['KNw', 'Pw', ' ', ' ', ' ', ' ', ' ', 'KNb'],
                                      ['Rw', ' ', 'Pb', ' ', ' ', ' ', 'Pb', 'Rb']])
#        self.assertEqual(len(game1.white_figures), 15)
#        self.assertEqual(len(game1.black_figures), 15)

    def tearDown(self):
        pass



class TestWin(unittest.TestCase):

    def setUp(self):
        pass

    def test_win(self):
        game1 = Game("w")
        game2 = Game("b")

        self.assertFalse(game1.isDrawMove("g2", "g4"))
        self.assertFalse(game1.isWinMove("g2", "g4"))
        self.assertTrue(game1.isPossibleMove("g2", "g4"))
        game1.move("g2", "g4")
        game2.move_from_server("g2", "g4")

        self.assertFalse(game2.isDrawMove("e7", "e5"))
        self.assertFalse(game2.isWinMove("e7", "e5"))
        self.assertTrue(game2.isPossibleMove("e7", "e5"))
        game2.move("e7", "e5")
        game1.move_from_server("e7", "e5")

        self.assertFalse(game1.isDrawMove("f2", "f3"))
        self.assertFalse(game1.isWinMove("f2", "f3"))
        self.assertTrue(game1.isPossibleMove("f2", "f3"))
        game1.move("f2", "f3")
        game2.move_from_server("f2", "f3")

        self.assertFalse(game2.isDrawMove("d8", "h4"))
        self.assertTrue(game2.isWinMove("d8", "h4"))
        self.assertTrue(game2.isPossibleMove("d8", "h4"))
        game2.move("d8", "h4")
        game1.move_from_server("d8", "h4")

        self.assertEqual(game1.board, [['Rw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Rb'],
                                       ['KNw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'KNb'],
                                       ['Bw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Bb'],
                                       ['Qw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', ' '],
                                       ['Kw', 'Pw', ' ', ' ', 'Pb', ' ', ' ', 'Kb'],
                                       ['Bw', ' ', 'Pw', ' ', ' ', ' ', 'Pb', 'Bb'],
                                       ['KNw', ' ', ' ', 'Pw', ' ', ' ', 'Pb', 'KNb'],
                                       ['Rw', 'Pw', ' ', 'Qb', ' ', ' ', 'Pb', 'Rb']])

    def tearDown(self):
        pass


class TestRightRoque(unittest.TestCase):

    def setUp(self):
        pass

    def test_right_roque(self):
        game1 = Game("w")
        game2 = Game("b")

        self.assertFalse(game1.isDrawMove("e2", "e4"))
        self.assertFalse(game1.isWinMove("e2", "e4"))
        self.assertTrue(game1.isPossibleMove("e2", "e4"))
        game1.move("e2", "e4")
        game2.move_from_server("e2", "e4")

        self.assertFalse(game2.isDrawMove("e7", "e5"))
        self.assertFalse(game2.isWinMove("e7", "e5"))
        self.assertTrue(game2.isPossibleMove("e7", "e5"))
        game2.move("e7", "e5")
        game1.move_from_server("e7", "e5")

        self.assertFalse(game1.isDrawMove("f1", "d3"))
        self.assertFalse(game1.isWinMove("f1", "d3"))
        self.assertTrue(game1.isPossibleMove("f1", "d3"))
        game1.move("f1", "d3")
        game2.move_from_server("f1", "d3")

        self.assertFalse(game2.isDrawMove("f8", "d6"))
        self.assertFalse(game2.isWinMove("f8", "d6"))
        self.assertTrue(game2.isPossibleMove("f8", "d6"))
        game2.move("f8", "d6")
        game1.move_from_server("f8", "d6")

        self.assertFalse(game1.isDrawMove("g1", "f3"))
        self.assertFalse(game1.isWinMove("g1", "f3"))
        self.assertTrue(game1.isPossibleMove("g1", "f3"))
        game1.move("g1", "f3")
        game2.move_from_server("g1", "f3")

        self.assertFalse(game2.isDrawMove("g8", "f6"))
        self.assertFalse(game2.isWinMove("g8", "f6"))
        self.assertTrue(game2.isPossibleMove("g8", "f6"))
        game2.move("g8", "f6")
        game1.move_from_server("g8", "f6")

        self.assertFalse(game1.isDrawMove("e1", "g1"))
        self.assertFalse(game1.isWinMove("e1", "g1"))
        self.assertTrue(game1.isPossibleMove("e1", "g1"))
        game1.move("e1", "g1")
        game2.move_from_server("e1", "g1")

        self.assertFalse(game2.isDrawMove("e8", "g8"))
        self.assertFalse(game2.isWinMove("e8", "g8"))
        self.assertTrue(game2.isPossibleMove("e8", "g8"))
        game2.move("e8", "g8")
        game1.move_from_server("e8", "g8")

        self.assertEqual(game1.board, [['Rw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Rb'],
                                       ['KNw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'KNb'],
                                       ['Bw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Bb'],
                                       ['Qw', 'Pw', 'Bw', ' ', ' ', 'Bb', 'Pb', 'Qb'],
                                       [' ', ' ', ' ', 'Pw', 'Pb', ' ', ' ', ' '],
                                       ['Rw', 'Pw', 'KNw', ' ', ' ', 'KNb', 'Pb', 'Rb'],
                                       ['Kw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Kb'],
                                       [' ', 'Pw', ' ', ' ', ' ', ' ', 'Pb', ' ']])

    def tearDown(self):
        pass


class TestLeftRoque(unittest.TestCase):

    def setUp(self):
        pass

    def test_left_roque(self):
        game1 = Game("w")
        game2 = Game("b")

        self.assertFalse(game1.isDrawMove("d2", "d4"))
        self.assertFalse(game1.isWinMove("d2", "d4"))
        self.assertTrue(game1.isPossibleMove("d2", "d4"))
        game1.move("d2", "d4")
        game2.move_from_server("d2", "d4")

        self.assertFalse(game2.isDrawMove("d7", "d5"))
        self.assertFalse(game2.isWinMove("d7", "d5"))
        self.assertTrue(game2.isPossibleMove("d7", "d5"))
        game2.move("d7", "d5")
        game1.move_from_server("d7", "d5")

        self.assertFalse(game1.isDrawMove("c1", "e3"))
        self.assertFalse(game1.isWinMove("c1", "e3"))
        self.assertTrue(game1.isPossibleMove("c1", "e3"))
        game1.move("c1", "e3")
        game2.move_from_server("c1", "e3")

        self.assertFalse(game2.isDrawMove("c8", "e6"))
        self.assertFalse(game2.isWinMove("c8", "e6"))
        self.assertTrue(game2.isPossibleMove("c8", "e6"))
        game2.move("c8", "e6")
        game1.move_from_server("c8", "e6")

        self.assertFalse(game1.isDrawMove("b1", "c3"))
        self.assertFalse(game1.isWinMove("b1", "c3"))
        self.assertTrue(game1.isPossibleMove("b1", "c3"))
        game1.move("b1", "c3")
        game2.move_from_server("b1", "c3")

        self.assertFalse(game2.isDrawMove("b8", "c6"))
        self.assertFalse(game2.isWinMove("b8", "c6"))
        self.assertTrue(game2.isPossibleMove("b8", "c6"))
        game2.move("b8", "c6")
        game1.move_from_server("b8", "c6")

        self.assertFalse(game1.isDrawMove("d1", "d2"))
        self.assertFalse(game1.isWinMove("d1", "d2"))
        self.assertTrue(game1.isPossibleMove("d1", "d2"))
        game1.move("d1", "d2")
        game2.move_from_server("d1", "d2")

        self.assertFalse(game2.isDrawMove("d8", "d7"))
        self.assertFalse(game2.isWinMove("d8", "d7"))
        self.assertTrue(game2.isPossibleMove("d8", "d7"))
        game2.move("d8", "d7")
        game1.move_from_server("d8", "d7")

        self.assertFalse(game1.isDrawMove("e1", "c1"))
        self.assertFalse(game1.isWinMove("e1", "c1"))
        self.assertTrue(game1.isPossibleMove("e1", "c1"))
        game1.move("e1", "c1")
        game2.move_from_server("e1", "c1")

        self.assertFalse(game2.isDrawMove("e8", "c8"))
        self.assertFalse(game2.isWinMove("e8", "c8"))
        self.assertTrue(game2.isPossibleMove("e8", "c8"))
        game2.move("e8", "c8")
        game1.move_from_server("e8", "c8")

        self.assertEqual(game1.board, [[' ', 'Pw', ' ', ' ', ' ', ' ', 'Pb', ' '],
                                       [' ', 'Pw', ' ', ' ', ' ', ' ', 'Pb', ' '],
                                       ['Kw', 'Pw', 'KNw', ' ', ' ', 'KNb', 'Pb', 'Kb'],
                                       ['Rw', 'Qw', ' ', 'Pw', 'Pb', ' ', 'Qb', 'Rb'],
                                       [' ', 'Pw', 'Bw', ' ', ' ', 'Bb', 'Pb', ' '],
                                       ['Bw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Bb'],
                                       ['KNw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'KNb'],
                                       ['Rw', 'Pw', ' ', ' ', ' ', ' ', 'Pb', 'Rb']])

    def tearDown(self):
        pass
