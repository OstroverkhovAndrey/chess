
import cmd
import threading
import time
import readline
import socket

class chess_client(cmd.Cmd):

    prompt = "chess >> "

    def __init__(self):
        super().__init__()
        self.socket = socket.socket()
        self.socket.connect(("0.0.0.0", 1337))
        self.timer = threading.Thread(target=self.read_from_server, args=())
        self.timer.start()

    def do_exit(self, arg):
        """Exit program"""
        return 1

    def do_EOF(self, arg):
        """Exit program"""
        return 1

    def write_to_server(self, data):
        self.socket.send(data.encode())

    def read_from_server(self):
        t = threading.current_thread()
        while True:
            data = self.socket.recv(1024).decode()
            print(data)


if __name__ == "__main__":
    chess_client().cmdloop()

