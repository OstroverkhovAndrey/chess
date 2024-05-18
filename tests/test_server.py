
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


class TestServerRegistre(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        chess_server.dump_user_info = MagicMock()

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}

    async def test_registre_ok(self):
        self.assertFalse("user_name" in chess_server.users)

        await chess_server.registre("user_name", "writer", "command_num")
        self.assertTrue("user_name" in chess_server.users)
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "registre_ok")
        chess_server.dump_user_info.assert_called_with(chess_server.users)

    async def test_registre_not(self):
        self.assertFalse("user_name" in chess_server.users)

        await chess_server.registre("user_name", "writer", "command_num")
        self.assertTrue("user_name" in chess_server.users)
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "registre_ok")
        chess_server.dump_user_info.assert_called_with(chess_server.users)

        await chess_server.registre("user_name", "writer", "command_num")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "registre_not")
        self.assertEqual(len(chess_server.send_msg.mock_calls), 2)
        self.assertEqual(len(chess_server.dump_user_info.mock_calls), 1)


class TestServerLogin(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        pass

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}
        chess_server.users["user_name"] = UserInfo("user_name")
        chess_server.users["user_name1"] = UserInfo("user_name1")
        chess_server.clients = {}

    async def test_success_login(self):
        self.assertTrue("user_name" in chess_server.users)
        self.assertEqual(chess_server.clients, {})
        chess_server.clients["me"] = ClientsInfo()
        await chess_server.login("user_name", "me", "writer", "command_num")

        self.assertEqual(chess_server.clients["me"].user_name, "user_name")
        self.assertTrue(chess_server.users["user_name"].isOnline)
        self.assertEqual(chess_server.users["user_name"].IP, "me")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "success_login")

    async def test_login_already_online(self):
        self.assertTrue("user_name" in chess_server.users)
        self.assertEqual(chess_server.clients, {})

        chess_server.clients["me"] = ClientsInfo()
        await chess_server.login("user_name", "me", "writer", "command_num")
        self.assertEqual(chess_server.clients["me"].user_name, "user_name")
        self.assertTrue(chess_server.users["user_name"].isOnline)
        self.assertEqual(chess_server.users["user_name"].IP, "me")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "success_login")

        chess_server.clients["me1"] = ClientsInfo()
        await chess_server.login("user_name", "me1", "writer", "command_num")
        self.assertEqual(chess_server.clients["me"].user_name, "user_name")
        self.assertTrue(chess_server.users["user_name"].isOnline)
        self.assertEqual(chess_server.users["user_name"].IP, "me")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "login_already_online")

    async def test_you_already_login(self):
        self.assertTrue("user_name" in chess_server.users)
        self.assertEqual(chess_server.clients, {})

        chess_server.clients["me"] = ClientsInfo()
        await chess_server.login("user_name", "me", "writer", "command_num")
        self.assertEqual(chess_server.clients["me"].user_name, "user_name")
        self.assertTrue(chess_server.users["user_name"].isOnline)
        self.assertEqual(chess_server.users["user_name"].IP, "me")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "success_login")

        await chess_server.login("user_name1", "me", "writer", "command_num")
        self.assertEqual(chess_server.clients["me"].user_name, "user_name")
        self.assertTrue(chess_server.users["user_name"].isOnline)
        self.assertEqual(chess_server.users["user_name"].IP, "me")
        self.assertFalse(chess_server.users["user_name1"].isOnline)
        self.assertEqual(chess_server.users["user_name1"].IP, "")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "already_login")

    async def test_login_dont_registre(self):
        self.assertTrue("user_name" in chess_server.users)
        self.assertEqual(chess_server.clients, {})
        chess_server.clients["me"] = ClientsInfo()
        await chess_server.login("user_name2", "me", "writer", "command_num")

        self.assertEqual(chess_server.clients["me"].user_name, "")
        self.assertFalse("user_name2" in chess_server.users)
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "login_dont_registre")
