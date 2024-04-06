
import asyncio

class ClientsInfo:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.user_name = ""

