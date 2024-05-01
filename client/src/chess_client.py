
import cmd
import threading
import readline
import socket
import shlex
from chess_game import Game


class chess_client(cmd.Cmd):

    prompt = "chess >> "

    def __init__(self):
        super().__init__()
        self.socket = socket.socket()
        self.socket.connect(("0.0.0.0", 1337))
        self.timer = threading.Thread(target=self.read_from_server, args=())
        self.timer.start()
        self.rn = 1
        self.cn = 2
        self.request = {}
        self.complition = {}
        self.game = None

    def request_num(self):
        self.rn += 2
        return self.rn

    def complition_num(self):
        self.cn += 2
        return self.cn

    def print_error_message(self, error=""):
        print(error)

    def do_registre(self, arg):
        """registre form chess server"""
        arg = shlex.split(arg)
        if len(arg) > 1:
            self.print_error_message("More arguments!")
        elif len(arg) < 1:
            self.print_error_message("Not enough arguments!")
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("registre " + arg[0] + "\n", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(self.request[num])

    def do_login(self, arg):
        """login from chess server"""
        arg = shlex.split(arg)
        if len(arg) > 1:
            self.print_error_message("More arguments!")
        elif len(arg) < 1:
            self.print_error_message("Not enough arguments!")
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("login " + arg[0] + "\n", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(self.request[num])

    def complete_login(self, text, line, begidx, endidx):
        """complete login command"""
        num = self.complition_num()
        self.complition[num] = None
        self.write_to_server("offline_users\n", num)

        while self.complition[num] is None:
            pass

        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                complition = self.complition[num].split()
        return [c for c in complition if c.startswith(text)]

    def do_logout(self, arg):
        """logout from chess server"""
        arg = shlex.split(arg)
        if len(arg) > 0:
            self.print_error_message("More arguments!")
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("logout\n", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(self.request[num])

    def do_get_users(self, arg):
        """get online users"""
        arg = shlex.split(arg)
        if len(arg) > 0:
            self.print_error_message("More arguments!")
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("online_users\n", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(self.request[num])

    def do_get_game_request(self, arg):
        """get game request from current player"""
        arg = shlex.split(arg)
        if len(arg) > 0:
            self.print_error_message("More arguments!")
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("game_request\n", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(self.request[num])

    def do_play(self, arg):
        """play request with another user"""
        arg = shlex.split(arg)
        if len(arg) > 1:
            self.print_error_message("More arguments!")
        elif len(arg) < 1:
            self.print_error_message("Not enough arguments!")
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("play " + arg[0] + "\n", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(self.request[num])

            if "start game" in self.request[num]:
                color = int(self.request[num][-1])
                color = "w" if not color else "b"
                self.game = Game(color)
                print(color)
                print(self.game.get_board())

    def complete_play(self, text, line, begidx, endidx):
        """complete play command"""
        num = self.complition_num()
        self.complition[num] = None
        self.write_to_server("online_users\n", num)

        while self.complition[num] is None:
            pass

        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                complition = self.complition[num].split()
        return [c for c in complition if c.startswith(text)]

    def do_move(self, arg):
        """move command"""
        arg = shlex.split(arg)
        if len(arg) > 1:
            self.print_error_message("More arguments!")
        elif len(arg) < 1:
            self.print_error_message("Not enough arguments!")
        else:
            if "to" not in arg[0]:
                print("Impossible move!")
                return
            move = arg[0]
            move = move.split("to")
            self.game.move(move[0], move[1])
            print(self.game.get_board())

            num = self.request_num()
            self.request[num] = None
            self.write_to_server("move " + arg[0] + "\n", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(self.request[num])

    def complete_move(self, text, line, begidx, endidx):
        """print all passible move"""
        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                for start, ends in self.game.get_possible_moves().items():
                    for end in ends:
                        complition.append(start+"to"+end)

        return [c for c in complition if c.startswith(text)]

    def do_exit(self, arg):
        """Exit program"""
        return 1

    def do_EOF(self, arg):
        """Exit program"""
        return 1

    def write_to_server(self, data, request_num):
        self.socket.send((str(request_num) + ": " + data).encode())

    def read_from_server(self):
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            data = self.socket.recv(1024).decode()
            data_num = data.split(":")[0]
            data = data[len(data_num)+1:].strip()
            data_num = int(data_num)
            if data_num in self.complition and\
                    self.complition[data_num] is None:
                self.complition[data_num] = data
            elif data_num in self.request and self.request[data_num] is None:
                self.request[data_num] = data
            else:
                if "start game" in data:
                    color = int(data[-1])
                    color = "w" if not color else "b"
                    self.game = Game(color)
                    board = self.game.get_board()
                    print(f"\n{data}\n{color}\n{board}\n{self.prompt}\
                          {readline.get_line_buffer()}", end="", flush=True)
                elif "opponent get move" in data:
                    move = data.split()[-1]
                    move = move.split("to")
                    self.game.move_from_server(move[0], move[1])
                    board = self.game.get_board()
                    print(f"\n{data}\n{board}\n{self.prompt}\
                          {readline.get_line_buffer()}",
                          end="", flush=True)
                else:
                    print(f"\n{data}\n{self.prompt}\
                          {readline.get_line_buffer()}", end="", flush=True)


if __name__ == "__main__":
    chess_client().cmdloop()
