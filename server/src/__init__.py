
"""Init."""

import os
import sys
sys.path.insert(1, os.path.dirname(__file__))
import asyncio
from dump_load import load_user_info
from dump_load import load_game_history
from chess_server import main
import chess_server


def server():
    """Run server."""
    print("Run server!")
    chess_server.users = load_user_info()
    chess_server.game_history = load_game_history()
    asyncio.run(main())
