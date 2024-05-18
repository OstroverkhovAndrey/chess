
"""Tests for client."""

import os
import sys
sys.path.insert(1, os.path.dirname(__file__) + '/../client/src/')
import unittest
from unittest.mock import MagicMock
import chess_client
import locale
import internationalization
from chess_game import Game
from server_answer import mock_for_i18n


def setUpModule():
    def __init__(self) -> None:
        """Init chess_client."""
        self.rn = 1
        self.cn = 2
        self.request = {}
        self.complet = {}
        self.name = ""
        self.game = None
        self.draw_request = False

    chess_client.chess_client.__init__ = __init__
    locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))


class TestGetNextNum(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

    def test_request_num(self):
        self.assertEqual(self.client.request_num(), 3)
        self.assertEqual(self.client.request_num(), 5)
        self.assertEqual(self.client.request_num(), 7)

    def test_complet_num(self):
        self.assertEqual(self.client.complet_num(), 4)
        self.assertEqual(self.client.complet_num(), 6)
        self.assertEqual(self.client.complet_num(), 8)


class TestRegistre(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "registre_ok"
        chess_client.chess_client.wait_request_ans = wait_request_ans

    def test_do_registre(self):
        self.client.do_registre("1 1")
        chess_client.print.assert_called_with("More arguments")
        self.client.do_registre("")
        chess_client.print.assert_called_with("Not enough arguments")
        self.client.do_registre("#@$")
        chess_client.print.assert_called_with("Incorrect name")

        self.client.do_registre("1")
        self.client.write_to_server.assert_called_with("registre 1", 3)
        chess_client.print.assert_called_with("Success registre")


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "success_login"
        chess_client.chess_client.wait_request_ans = wait_request_ans

        def wait_complet_ans(self, num):
            self.complet[num] = "1 2 3"
        chess_client.chess_client.wait_complet_ans = wait_complet_ans

    def test_do_login(self):
        self.client.do_login("1 1")
        chess_client.print.assert_called_with("More arguments")
        self.client.do_login("")
        chess_client.print.assert_called_with("Not enough arguments")
        self.client.do_login("#@$")
        chess_client.print.assert_called_with("Incorrect name")

        self.client.do_login("1")
        self.client.write_to_server.assert_called_with("login 1", 3)
        chess_client.print.assert_called_with("Success login")
        self.client.do_login("1")
        self.assertEqual(len(self.client.write_to_server.mock_calls), 1)
        chess_client.print.assert_called_with("You already login")

    def test_complet_login(self):
        self.assertEqual(self.client.complete_login("", "login ", 6, 6),
                         ["1", "2", "3"])
        self.client.write_to_server.assert_called_with("offline_users", 4)


class TestLogout(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "success_logout"
        chess_client.chess_client.wait_request_ans = wait_request_ans

    def test_do_logout(self):
        self.client.do_logout("1 1")
        chess_client.print.assert_called_with("More arguments")

        self.client.do_logout("")
        chess_client.print.assert_called_with("You dont login")

        self.client.name = "1"
        self.client.do_logout("")
        self.client.write_to_server.assert_called_with("logout", 3)
        chess_client.print.assert_called_with("Success logout")


class TestGetUsers(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "a b c"
        chess_client.chess_client.wait_request_ans = wait_request_ans

    def test_do_get_users(self):
        self.client.do_get_users("1 1")
        chess_client.print.assert_called_with("More arguments")

        self.client.do_get_users("")
        self.client.write_to_server.assert_called_with("online_users", 3)
        chess_client.print.assert_called_with("a b c")


class TestGetGameRequest(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "game_request.1.2 3 4"
        chess_client.chess_client.wait_request_ans = wait_request_ans

    def test_do_get_game_request(self):
        self.client.do_get_game_request("1 1")
        chess_client.print.assert_called_with("More arguments")

        self.client.do_get_game_request("")
        self.client.write_to_server.assert_called_with("game_request", 3)
        chess_client.print.assert_called_with("From me: 1\nFor me: 2 3 4")


class TestRemoveGameRequest(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "success_remove_game_request"
        chess_client.chess_client.wait_request_ans = wait_request_ans

    def test_do_remove_game_request(self):
        self.client.do_remove_game_request("a")
        chess_client.print.assert_called_with("More arguments")

        self.client.do_remove_game_request("")
        self.client.write_to_server.assert_called_with("remove_game_request", 3)
        chess_client.print.assert_called_with("Success remove game request")


class TestGetStatistic(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "statistic.1.2.3.4"
        chess_client.chess_client.wait_request_ans = wait_request_ans

    def test_do_statistic(self):
        self.client.do_get_statistic("1 1")
        chess_client.print.assert_called_with("More arguments")

        self.client.do_get_statistic("1")
        self.client.write_to_server.assert_called_with("statistic 1", 3)
        chess_client.print.assert_called_with(
            "Statistic for 1\nwin: 2\ndraw: 3\ndefeat: 4")


class TestPlay(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            if num == 3:
                self.request[num] = "send_game_request"
            else:
                self.request[num] = "start_game 0"
        chess_client.chess_client.wait_request_ans = wait_request_ans

        def wait_complet_ans(self, num):
            self.complet[num] = "1 2 3"
        chess_client.chess_client.wait_complet_ans = wait_complet_ans

    def test_do_play(self):
        self.client.do_play("1 1")
        chess_client.print.assert_called_with("More arguments")
        self.client.do_play("")
        chess_client.print.assert_called_with("Not enough arguments")
        self.client.do_play("#@$")
        chess_client.print.assert_called_with("Incorrect name")

        self.client.do_play("1")
        self.client.write_to_server.assert_called_with("play 1", 3)
        chess_client.print.assert_called_with("Send game request")

        self.client.do_play("1")
        self.client.write_to_server.assert_called_with("play 1", 5)
        self.assertEqual(chess_client.print.mock_calls[-2].args[0],
                         "Start game, color: w")

    def test_complet_play(self):
        self.assertEqual(self.client.complete_play("", "play ", 5, 5),
                         ["1", "2", "3"])
        self.client.write_to_server.assert_called_with("online_users", 4)


class TestMove(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "you_get_move"
        chess_client.chess_client.wait_request_ans = wait_request_ans

        def get_possible_moves():
            return {"e2": ["e3", "e4"], "a2": ["a3", "a4"], }
        self.client.game = Game("w")
        self.client.game.get_possible_moves = get_possible_moves

    def test_do_move_error(self):
        self.client.game = None
        self.client.do_move("e2e4")
        chess_client.print.assert_called_with("You dont play now")

        self.client.game = Game("b")
        self.client.do_move("e2e4")
        chess_client.print.assert_called_with("Now not you move")

        self.client.game = Game("w")
        self.client.do_move("e2 to e4")
        chess_client.print.assert_called_with("More arguments")

        self.client.do_move("")
        chess_client.print.assert_called_with("Not enough arguments")

        self.client.draw_request = True
        self.client.do_move("e2e4")
        chess_client.print.assert_called_with("You send draw request")

        self.client.draw_request = False
        self.client.do_move("e2toe4")
        chess_client.print.assert_called_with("Incorrect move")

    def test_do_move(self):

        self.client.game.isPossibleMove = MagicMock(return_value=False)
        self.client.do_move("e2e4")
        chess_client.print.assert_called_with("It is impossiple move")

        self.client.game = Game("w")
        self.client.game.isPossibleMove = MagicMock(return_value=True)
        self.client.game.isWinMove = MagicMock(return_value=False)
        self.client.game.isDrawMove = MagicMock(return_value=False)
        self.client.do_move("e2e4")
        self.client.write_to_server.assert_called_with("move e2e4:ok", 3)
        chess_client.print.assert_called_with("You get move")

        self.client.game = Game("w")
        self.client.game.isPossibleMove = MagicMock(return_value=True)
        self.client.game.isWinMove = MagicMock(return_value=True)
        self.client.game.isDrawMove = MagicMock(return_value=False)
        self.client.do_move("e2e4")
        self.assertEqual(self.client.write_to_server.mock_calls[-1].args,
                         ("move e2e4:win", 5))
        self.assertEqual(chess_client.print.mock_calls[-2].args[0],
                         "You get move")
        self.assertEqual(chess_client.print.mock_calls[-1].args[0],
                         "Stop game, you win!")
        self.assertIsNone(self.client.game)

        self.client.game = Game("w")
        self.client.game.isPossibleMove = MagicMock(return_value=True)
        self.client.game.isWinMove = MagicMock(return_value=False)
        self.client.game.isDrawMove = MagicMock(return_value=True)
        self.client.do_move("e2e4")
        self.assertEqual(self.client.write_to_server.mock_calls[-1].args,
                         ("move e2e4:draw", 7))
        self.assertEqual(chess_client.print.mock_calls[-2].args[0],
                         "You get move")
        self.assertEqual(chess_client.print.mock_calls[-1].args[0],
                         "Stop game, draw")
        self.assertIsNone(self.client.game)

    def test_complet_move(self):
        self.assertEqual(self.client.complete_move("e", "move e", 6, 6),
                         ["e2e3", "e2e4"])


class TestDraw(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            if num == 3:
                self.request[num] = "send_draw_request"
            else:
                self.request[num] = "draw"
        chess_client.chess_client.wait_request_ans = wait_request_ans
        self.client.game = Game("w")

    def test_do_draw(self):
        self.client.game = None
        self.client.do_draw("ok")
        chess_client.print.assert_called_with("You dont play now")

        self.client.game = Game("w")
        self.client.do_draw("ok not")
        chess_client.print.assert_called_with("More arguments")

        self.client.do_draw("")
        chess_client.print.assert_called_with("Not enough arguments")

        self.client.do_draw("yes")
        chess_client.print.assert_called_with("Incorrect argument")

        self.client.do_draw("ok")
        self.assertEqual(self.client.write_to_server.mock_calls[-1].args,
                         ("draw ok", 3))
        chess_client.print.assert_called_with("Send draw request")

        self.client.do_draw("ok")
        self.assertEqual(self.client.write_to_server.mock_calls[-1].args,
                         ("draw ok", 5))
        chess_client.print.assert_called_with("Draw")

    def test_complet_draw(self):
        self.assertEqual(self.client.complete_draw("", "draw ", 5, 5),
                         ["ok", "not"])


class TestGiveUp(unittest.TestCase):

    def setUp(self):
        self.client = chess_client.chess_client()
        chess_client.print = MagicMock()
        chess_client.chess_client.write_to_server = MagicMock()

        def wait_request_ans(self, num):
            self.request[num] = "you_success_give_up"
        chess_client.chess_client.wait_request_ans = wait_request_ans
        self.client.game = Game("w")

    def test_do_give_up(self):
        self.client.game = None
        self.client.do_give_up("")
        chess_client.print.assert_called_with("You dont play now")

        self.client.game = Game("w")
        self.client.do_give_up("ok not")
        chess_client.print.assert_called_with("More arguments")

        self.client.do_give_up("")
        self.assertEqual(self.client.write_to_server.mock_calls[-1].args,
                         ("give_up", 3))
        chess_client.print.assert_called_with("You success give up")
