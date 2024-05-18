
"""Tests for dump/load functions."""

import os
import sys
sys.path.insert(1, os.path.dirname(__file__) + '/../server/src/')
import unittest
import server.src.dump_load as dump_load
from server.src.user_info import UserInfo
from server.src.game_history import GameHistory
from server.src.dump_load import dump_user_info, load_user_info
from server.src.dump_load import dump_game_history, load_game_history


class TestDumpLoad(unittest.TestCase):

    def setUp(self):
        if os.path.exists(dump_load.dump_path + dump_load.user_info_dump):
            os.remove(dump_load.dump_path + dump_load.user_info_dump)
        if os.path.exists(dump_load.dump_path + dump_load.game_history_dump):
            os.remove(dump_load.dump_path + dump_load.game_history_dump)
        if os.path.exists(dump_load.dump_path):
            os.rmdir(dump_load.dump_path)
        dump_load.dump_path = os.path.dirname(__file__) + "/dump/"

        self.users = {}
        self.users["1"] = UserInfo("1")
        self.users["2"] = UserInfo("2")
        self.users["3"] = UserInfo("3")

        self.game_history = GameHistory()
        self.game_history.add_game("1", "2", "1", "")
        self.game_history.add_game("1", "3", "3", "")
        self.game_history.add_game("4", "1", "draw", "")
        self.game_history.add_game("2", "1", "1", "")
        self.game_history.add_game("3", "2", "3", "")

    def test_user_info(self):
        dump_user_info(self.users)
        load_users = load_user_info()
        self.assertTrue("1" in load_users)
        self.assertFalse(load_users["1"].isOnline)
        self.assertFalse(load_users["1"].isPlay)
        self.assertTrue("2" in load_users)
        self.assertTrue("3" in load_users)

    def test_user_info_empty(self):
        if os.path.exists(dump_load.dump_path + dump_load.user_info_dump):
            os.remove(dump_load.dump_path + dump_load.user_info_dump)
        load_users = load_user_info()
        self.assertEqual(load_users, {})

    def test_game_history(self):
        dump_game_history(self.game_history)
        load_history = load_game_history()
        self.assertEqual(load_history.get_statistic_for_user("1"), [2, 1, 1])
        self.assertEqual(load_history.get_statistic_for_user("2"), [0, 0, 3])
        self.assertEqual(load_history.get_statistic_for_user("3"), [2, 0, 0])
        self.assertEqual(load_history.get_statistic_for_user("4"), [0, 1, 0])
        self.assertEqual(load_history.get_statistic_for_user("5"), [0, 0, 0])

    def test_game_history_empty(self):
        if os.path.exists(dump_load.dump_path + dump_load.game_history_dump):
            os.remove(dump_load.dump_path + dump_load.game_history_dump)
        load_history = load_game_history()
        self.assertEqual(load_history.history, [])

    def tearDown(self):
        if os.path.exists(dump_load.dump_path + dump_load.user_info_dump):
            os.remove(dump_load.dump_path + dump_load.user_info_dump)
        if os.path.exists(dump_load.dump_path + dump_load.game_history_dump):
            os.remove(dump_load.dump_path + dump_load.game_history_dump)
        if os.path.exists(dump_load.dump_path):
            os.rmdir(dump_load.dump_path)
