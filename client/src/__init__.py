
"""Init."""

import os
import sys
sys.path.insert(1, os.path.dirname(__file__))
from chess_client import chess_client
from internationalization import _


def client():
    """Run client."""
    print("Run client!")
    try:
        chess_client().cmdloop()
    except ConnectionRefusedError:
        print(_("The server is currently unavailable, please try again later"))
