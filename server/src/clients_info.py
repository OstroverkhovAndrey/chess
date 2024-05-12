
"""Module for storing information about users connected to the server."""

import asyncio


class ClientsInfo:
    """Information about users connected to the server."""

    def __init__(self):
        """Init ClientsInfo, set asyncio.Queue and empty user_name."""
        self.queue = asyncio.Queue()
        self.user_name = ""
