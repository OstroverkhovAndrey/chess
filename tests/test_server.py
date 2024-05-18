
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


class TestGameRequest(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        pass

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}
        chess_server.clients = {}

        chess_server.clients["me1"] = ClientsInfo()
        chess_server.clients["me1"].user_name = "1"
        chess_server.clients["me2"] = ClientsInfo()
        chess_server.clients["me2"].user_name = "2"
        chess_server.clients["me3"] = ClientsInfo()
        chess_server.clients["me3"].user_name = "3"
        chess_server.clients["me4"] = ClientsInfo()
        chess_server.clients["me4"].user_name = "4"
        chess_server.game_request = {"1": "2",
                                     "2": "3",
                                     "3": "1",
                                     "4": "2", }

    async def test_get_game_request(self):
        await chess_server.get_game_request("me1", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "game_request.2.3")

        await chess_server.get_game_request("me2", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "game_request.3.1 4")

        await chess_server.get_game_request("me3", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "game_request.1.2")

        await chess_server.get_game_request("me4", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "game_request.2.")

    async def test_remove_game_request(self):
        await chess_server.remove_game_request("me2", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "success_remove_game_request")
        self.assertFalse("2" in chess_server.game_request)

        await chess_server.remove_game_request("me2", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "not_found_you_game_request")


class TestGetStatistic(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        pass

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}
        chess_server.clients = {}

        chess_server.clients["me1"] = ClientsInfo()
        chess_server.clients["me1"].user_name = "1"
        chess_server.clients["me2"] = ClientsInfo()
        chess_server.clients["me2"].user_name = "2"
        chess_server.clients["me3"] = ClientsInfo()
        chess_server.clients["me3"].user_name = "3"
        chess_server.clients["me4"] = ClientsInfo()
        chess_server.clients["me4"].user_name = "4"

        chess_server.game_history.add_game("1", "2", "1", "")
        chess_server.game_history.add_game("1", "3", "3", "")
        chess_server.game_history.add_game("4", "1", "draw", "")
        chess_server.game_history.add_game("2", "1", "1", "")
        chess_server.game_history.add_game("3", "2", "3", "")

    async def test_get_statistic(self):
        await chess_server.get_statistic("me1", "writer", "comand_num", "")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "statistic.1.2.1.1")

        await chess_server.get_statistic("me1", "writer", "comand_num", "1")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "statistic.1.2.1.1")

        await chess_server.get_statistic("me2", "writer", "comand_num", "2")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "statistic.2.0.0.3")

        await chess_server.get_statistic("me3", "writer", "comand_num", "3")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "statistic.3.2.0.0")

        await chess_server.get_statistic("me4", "writer", "comand_num", "")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "statistic.4.0.1.0")


class TestPlayCommand(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        pass

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}
        chess_server.clients = {}

        chess_server.users["1"] = UserInfo("1")
        chess_server.users["1"].isOnline = True
        chess_server.clients["me1"] = ClientsInfo()
        chess_server.clients["me1"].user_name = "1"

        chess_server.users["2"] = UserInfo("2")
        chess_server.users["2"].isOnline = True
        chess_server.users["2"].isPlay = True
        chess_server.clients["me2"] = ClientsInfo()
        chess_server.clients["me2"].user_name = "2"

        chess_server.clients["me3"] = ClientsInfo()

        chess_server.users["4"] = UserInfo("4")

        chess_server.users["5"] = UserInfo("5")
        chess_server.users["5"].IP = "me5"
        chess_server.users["5"].isOnline = True
        chess_server.clients["me5"] = ClientsInfo()
        chess_server.clients["me5"].user_name = "5"
        chess_server.clients["me5"].queue.put = AsyncMock()

        chess_server.users["6"] = UserInfo("6")
        chess_server.users["6"].isOnline = True
        chess_server.clients["me6"] = ClientsInfo()
        chess_server.clients["me6"].user_name = "6"

        chess_server.game_request["5"] = "6"

        chess_server.users["7"] = UserInfo("7")
        chess_server.users["7"].isOnline = True
        chess_server.clients["me7"] = ClientsInfo()
        chess_server.clients["me7"].user_name = "7"

        chess_server.random.randint = MagicMock(return_value=0)

    async def test_me_not_login(self):
        await chess_server.play("opponent", "me3", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_dont_login")

    async def test_opponent_dont_registre(self):
        await chess_server.play("55", "me1", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "opponent_dont_registre")

    async def test_opponent_dont_online(self):
        await chess_server.play("4", "me1", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "opponent_dont_online")

    async def test_play_with_yourself(self):
        await chess_server.play("1", "me1", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "cant_play_with_yourself")

    async def test_opponent_play(self):
        await chess_server.play("2", "me1", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "now_opponent_play")

    async def test_you_play(self):
        await chess_server.play("1", "me2", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "now_you_play")

    async def test_start_game(self):
        await chess_server.play("5", "me6", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "start_game 0")
        chess_server.clients["me5"].queue.put.assert_called_with("start_game 1")

    async def test_send_game_request(self):
        await chess_server.play("5", "me7", "writer", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "send_game_request")
        chess_server.clients["me5"].queue.put.assert_called_with(
            "send_you_game_request 7")


class TestMoveCommand(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        pass

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}
        chess_server.clients = {}

        chess_server.clients["me1"] = ClientsInfo()

        chess_server.users["2"] = UserInfo("2")
        chess_server.users["2"].isOnline = True
        chess_server.clients["me2"] = ClientsInfo()
        chess_server.clients["me2"].user_name = "2"

        chess_server.users["5"] = UserInfo("5")
        chess_server.users["5"].IP = "me5"
        chess_server.users["5"].isOnline = True
        chess_server.users["5"].isPlay = True
        chess_server.clients["me5"] = ClientsInfo()
        chess_server.clients["me5"].user_name = "5"
        chess_server.clients["me5"].queue.put = AsyncMock()

        chess_server.users["6"] = UserInfo("6")
        chess_server.users["6"].IP = "me6"
        chess_server.users["6"].isOnline = True
        chess_server.users["6"].isPlay = True
        chess_server.clients["me6"] = ClientsInfo()
        chess_server.clients["me6"].user_name = "6"

        chess_server.games.add_game("5", "6")
        chess_server.games["5"].set_draw_request("5")
        chess_server.print = MagicMock()

    async def test_me_not_login(self):
        await chess_server.move_command("me1", "writer", "move", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_dont_login")

    async def test_me_dont_play(self):
        await chess_server.move_command("me2", "writer", "move", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_dont_play_now")

    async def test_error_with_draw_request_in_client(self):
        await chess_server.move_command("me5", "writer", "move", "comand_num")
        chess_server.print.assert_called_with("Error with draw request!")

    async def test_move_and_refused_draw(self):
        await chess_server.move_command("me6", "writer", "move", "comand_num")
        self.assertEqual(chess_server.clients["me5"].queue.put.mock_calls[0].
                         args[0], "move_opponent_refused_draw")

    async def test_move(self):
        await chess_server.move_command("me6", "writer", "move", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_get_move")
        self.assertEqual(chess_server.clients["me5"].queue.put.mock_calls[1].
                         args[0], "opponent_get_move move")

    async def test_draw(self):
        await chess_server.move_command(
            "me6", "writer", "move:draw", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_get_move")
        self.assertEqual(chess_server.clients["me5"].queue.put.mock_calls[1].
                         args[0], "opponent_get_move move:draw")
        chess_server.print.assert_called_with("end game ", "draw")
        self.assertFalse(chess_server.users["5"].isPlay)
        self.assertFalse(chess_server.users["6"].isPlay)

    async def test_win(self):
        await chess_server.move_command(
            "me6", "writer", "move:win", "comand_num")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_get_move")
        self.assertEqual(chess_server.clients["me5"].queue.put.mock_calls[1].
                         args[0], "opponent_get_move move:win")
        chess_server.print.assert_called_with("end game ", "win")
        self.assertFalse(chess_server.users["5"].isPlay)
        self.assertFalse(chess_server.users["6"].isPlay)


class TestDrawCommand(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        pass

    async def asyncSetUp(self):
        chess_server.send_msg = AsyncMock()
        chess_server.users = {}
        chess_server.clients = {}

        chess_server.clients["me1"] = ClientsInfo()

        chess_server.users["2"] = UserInfo("2")
        chess_server.users["2"].isOnline = True
        chess_server.clients["me2"] = ClientsInfo()
        chess_server.clients["me2"].user_name = "2"

        chess_server.users["5"] = UserInfo("5")
        chess_server.users["5"].IP = "me5"
        chess_server.users["5"].isOnline = True
        chess_server.users["5"].isPlay = True
        chess_server.clients["me5"] = ClientsInfo()
        chess_server.clients["me5"].user_name = "5"
        chess_server.clients["me5"].queue.put = AsyncMock()

        chess_server.users["6"] = UserInfo("6")
        chess_server.users["6"].IP = "me6"
        chess_server.users["6"].isOnline = True
        chess_server.users["6"].isPlay = True
        chess_server.clients["me6"] = ClientsInfo()
        chess_server.clients["me6"].user_name = "6"
        chess_server.clients["me6"].queue.put = AsyncMock()

        chess_server.games.add_game("5", "6")
        chess_server.print = MagicMock()

    async def test_me_not_login(self):
        await chess_server.draw("me1", "writer", "comand_num", "msg")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_dont_login")

    async def test_me_dont_play(self):
        await chess_server.draw("me2", "writer", "comand_num", "msg")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_dont_play_now")

    async def test_send_draw_request_ok(self):
        await chess_server.draw("me5", "writer", "comand_num", "ok")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "send_draw_request")
        self.assertEqual(chess_server.games["5"].draw_request, "5")
        chess_server.clients["me6"].queue.put.assert_called_with(
            "opponent_send_you_draw_request")

    async def test_send_draw_request_not(self):
        await chess_server.draw("me5", "writer", "comand_num", "not")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "opponent_dont_send_draw_request")
        self.assertEqual(chess_server.games["5"].draw_request, None)

    async def test_repeat_send_draw_request_ok(self):
        chess_server.games["5"].draw_request = "5"
        await chess_server.draw("me5", "writer", "comand_num", "ok")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "send_draw_request")
        self.assertEqual(chess_server.games["5"].draw_request, "5")

    async def test_repeat_send_draw_request_not(self):
        chess_server.games["5"].draw_request = "5"
        await chess_server.draw("me5", "writer", "comand_num", "not")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_cant_delete_draw_request")
        self.assertEqual(chess_server.games["5"].draw_request, "5")

    async def test_ans_draw_request_ok(self):
        chess_server.games["5"].draw_request = "5"
        await chess_server.draw("me6", "writer", "comand_num", "ok")
        chess_server.send_msg.assert_called_with("writer", "comand_num", "draw")
        chess_server.clients["me5"].queue.put.assert_called_with("draw")
        self.assertFalse(chess_server.users["5"].isPlay)
        self.assertFalse(chess_server.users["6"].isPlay)

    async def test_ans_draw_request_not(self):
        chess_server.games["5"].draw_request = "5"
        await chess_server.draw("me6", "writer", "comand_num", "not")
        chess_server.send_msg.assert_called_with(
            "writer", "comand_num", "you_refused_draw")
        chess_server.clients["me5"].queue.put.assert_called_with(
            "opponent_refused_draw")
