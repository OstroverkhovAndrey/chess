
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
