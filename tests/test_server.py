
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


class TestServerLogout(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        pass

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}
        chess_server.users["user_name"] = UserInfo("user_name")
        chess_server.users["user_name"].isOnline = True
        chess_server.users["user_name"].IP = "me"
        chess_server.users["opponent"] = UserInfo("opponent")
        chess_server.users["opponent"].isOnline = True
        chess_server.users["opponent"].IP = "me_opponent"
        chess_server.clients = {}
        chess_server.clients["me"] = ClientsInfo()
        chess_server.clients["me"].user_name = "user_name"
        chess_server.clients["me_opponent"] = ClientsInfo()
        chess_server.clients["me_opponent"].user_name = "opponent"
        chess_server.game_request = {}
        chess_server.games = GamesDict()
        chess_server.game_history = GameHistory()

    async def test_success_logout(self):
        self.assertTrue(chess_server.users["user_name"].isOnline)
        self.assertTrue(chess_server.isOnline("me"))

        await chess_server.logout("me", "writer", "command_num")

        self.assertFalse(chess_server.users["user_name"].isOnline)
        self.assertEqual(chess_server.clients["me"].user_name, "")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "success_logout")

    async def test_logout_not(self):
        self.assertTrue(chess_server.users["user_name"].isOnline)
        self.assertTrue(chess_server.isOnline("me"))

        await chess_server.logout("me", "writer", "command_num")
        self.assertFalse(chess_server.users["user_name"].isOnline)
        self.assertEqual(chess_server.clients["me"].user_name, "")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "success_logout")

        await chess_server.logout("me", "writer", "command_num")
        self.assertFalse(chess_server.users["user_name"].isOnline)
        self.assertEqual(chess_server.clients["me"].user_name, "")
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "logout_not")

    async def test_success_logout_and_give_up(self):
        self.assertTrue(chess_server.users["user_name"].isOnline)
        self.assertTrue(chess_server.isOnline("me"))
        chess_server.users["user_name"].isPlay = True
        chess_server.users["opponent"].isPlay = True
        chess_server.games.add_game("user_name", "opponent")

        await chess_server.logout("me", "writer", "command_num")

        self.assertFalse(chess_server.users["user_name"].isOnline)
        self.assertFalse(chess_server.users["user_name"].isPlay)
        self.assertEqual(chess_server.clients["me"].user_name, "")
        self.assertTrue(unittest.mock.call(
            'writer', 0, 'success_logout_give_up') in
                chess_server.send_msg.mock_calls)
        chess_server.send_msg.assert_called_with(
            "writer", "command_num", "success_logout")


class TestGetUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        pass

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}
        chess_server.clients = {}

        chess_server.users["user_name"] = UserInfo("user_name")
        chess_server.users["user_name"].isOnline = True
        chess_server.users["user_name"].IP = "me"
        chess_server.clients["me"] = ClientsInfo()
        chess_server.clients["me"].user_name = "user_name"

        chess_server.users["user_name_1"] = UserInfo("user_name_1")
        chess_server.users["user_name_1"].isOnline = True
        chess_server.users["user_name_1"].IP = "me_1"
        chess_server.clients["me_1"] = ClientsInfo()
        chess_server.clients["me_1"].user_name = "user_name_1"

        chess_server.users["user_name_2"] = UserInfo("user_name_2")
        chess_server.users["user_name_2"].isOnline = False
        chess_server.users["user_name_2"].IP = ""
        chess_server.clients["me_2"] = ClientsInfo()
        chess_server.clients["me_2"].user_name = ""

    async def test_get_offline_users(self):
        await chess_server.get_offline_users("writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "user_name_2")

    async def test_get_online_users(self):
        await chess_server.get_online_users("writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "user_name user_name_1")
