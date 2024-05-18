
"""
Module for dump/load data.

Functions in module dumping and loading server data that should be saved when
the server is restared.
"""

from .user_info import UserInfo
from .game_history import GameHistory
import pickle
import os

dump_path = os.path.dirname(__file__) + "/../dump/"
user_info_dump = "user_info_dump"
game_history_dump = "game_history_dump"


def dump_user_info(users: dict) -> None:
    """
    Dump dict with information about users.

    Parameters
    ----------
    users : dict
        users, dict user_name -> UserInfo

    Returns
    -------
    None
    """
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)
    user_names = list(users.keys())
    with open(dump_path + user_info_dump, "wb") as file:
        pickle.dump(user_names, file)


def load_user_info() -> dict:
    """
    Load information about users from dump.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        dict user_name -> UserInfo
    """
    if not os.path.isfile(dump_path + user_info_dump):
        return {}
    with open(dump_path + user_info_dump, "rb") as file:
        user_names = pickle.load(file)
    users = {}
    for name in user_names:
        users[name] = UserInfo(name)
    return users


def dump_game_history(game_history: GameHistory) -> None:
    """
    Dump GameHistory class.

    Parameters
    ----------
    game_history : GameHistory
        History of the games played

    Returns
    -------
    None
    """
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)
    with open(dump_path + game_history_dump, "wb") as file:
        pickle.dump(game_history.history, file)


def load_game_history() -> GameHistory:
    """
    Load information about games played.

    Parameters
    ----------
    None

    Returns
    -------
    GameHistory
        GameHistory about games played
    """
    if not os.path.isfile(dump_path + game_history_dump):
        return GameHistory()
    with open(dump_path + game_history_dump, "rb") as file:
        history = pickle.load(file)
    game_history = GameHistory()
    game_history.history = history
    return game_history
