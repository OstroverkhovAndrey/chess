
"""Tests for server."""
import server.src.chess_server as chess_server
import unittest
from unittest.mock import AsyncMock, MagicMock
from server.src.clients_info import ClientsInfo
from server.src.user_info import UserInfo
from server.src.games import GamesDict
from server.src.game_history import GameHistory


class TestGetMsgNum(unittest.TestCase):

    def test_msg_with_num(self):
        num, msg = chess_server.get_msg_num("12: msg\n")
        self.assertEqual(num, 12)
        self.assertEqual(msg, msg)

    def test_msg_without_num(self):
        num, msg = chess_server.get_msg_num(" msg\n")
        self.assertEqual(num, 0)
        self.assertEqual(msg, msg)
