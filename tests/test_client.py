
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
