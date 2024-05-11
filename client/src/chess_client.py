
import cmd
import threading
import readline
import socket
import shlex
from chess_game import Game
from localization import _
from server_answer import server_answer


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
        self.name = ""
        self.game = None
        self.draw_request = False

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
            self.print_error_message(_("More arguments"))
        elif len(arg) < 1:
            self.print_error_message(_("Not enough arguments"))
        elif not arg[0].isalnum():
            self.print_error_message(_("Incorrect name"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("registre " + arg[0], num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(_(server_answer[self.request[num]]))

    def do_login(self, arg):
        """login from chess server"""
        arg = shlex.split(arg)
        if len(arg) > 1:
            self.print_error_message(_("More arguments"))
        elif len(arg) < 1:
            self.print_error_message(_("Not enough arguments"))
        elif not arg[0].isalnum():
            self.print_error_message(_("Incorrect name"))
        elif self.name != "":
            self.print_error_message(_("You already login"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("login " + arg[0], num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                if self.request[num] == "success_login":
                    self.name = arg[0]
                print(_(server_answer[self.request[num]]))

    def complete_login(self, text, line, begidx, endidx):
        """complete login command"""
        num = self.complition_num()
        self.complition[num] = None
        self.write_to_server("offline_users", num)

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
            self.print_error_message(_("More arguments"))
        elif self.name == "":
            self.print_error_message(_("You dont login"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("logout", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                if self.request[num] == "success_logout":
                    self.name = arg[0]
                print(_(server_answer[self.request[num]]))

    def do_get_users(self, arg):
        """get online users"""
        arg = shlex.split(arg)
        if len(arg) > 0:
            self.print_error_message(_("More arguments"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("online_users", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(self.request[num])

    def do_get_game_request(self, arg):
        """get game request from current player"""
        arg = shlex.split(arg)
        if len(arg) > 0:
            self.print_error_message(_("More arguments"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("game_request", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                msg, from_me, for_me = self.request[num].split(".")
                print(_(server_answer[msg]).format(from_me, for_me))

    def do_remove_game_request(self, arg):
        """remove game request which me sent"""
        if len(arg) > 0:
            self.print_error_message(_("More arguments"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("remove_game_request", num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(_(server_answer[self.request[num]]))

    def do_get_statistic(self, arg):
        """get statistic for current player or other player"""
        arg = shlex.split(arg)
        if len(arg) > 1:
            self.print_error_message(_("More arguments"))
        else:
            user = ""
            if len(arg) == 1 and arg[0].isalnum():
                user = arg[0]
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("statistic " + user, num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                msg, user_name, win, draw, defeat = self.request[num].split(".")
                print(_(server_answer[msg]).format(
                    user_name, win, draw, defeat))

    def do_play(self, arg):
        """play request with another user"""
        arg = shlex.split(arg)
        if len(arg) > 1:
            self.print_error_message(_("More arguments"))
        elif len(arg) < 1:
            self.print_error_message(_("Not enough arguments"))
        elif not arg[0].isalnum():
            self.print_error_message(_("Incorrect name"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("play " + arg[0], num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                if "start_game" in self.request[num]:
                    color = int(self.request[num].split()[-1][0])
                    msg = self.request[num].split()[0]
                    color = "w" if not color else "b"
                    self.game = Game(color)
                    print(_(server_answer[msg]).format(color))
                    print(self.game.get_board())
                else:
                    print(_(server_answer[self.request[num]]))

    def complete_play(self, text, line, begidx, endidx):
        """complete play command"""
        num = self.complition_num()
        self.complition[num] = None
        self.write_to_server("online_users", num)

        while self.complition[num] is None:
            pass

        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                complition = self.complition[num].split()
        return [c for c in complition if c.startswith(text) and c != self.name]

    def do_move(self, arg):
        """move command"""
        arg = shlex.split(arg)
        if self.game is None:
            self.print_error_message(_("You dont play now"))
        elif not self.game.isMyMove():
            self.print_error_message(_("Now not you move"))
        elif len(arg) > 1:
            self.print_error_message(_("More arguments"))
        elif len(arg) < 1:
            self.print_error_message(_("Not enough arguments"))
        elif self.draw_request:
            self.print_error_message(_("You send draw request"))
        elif len(arg[0]) != 4:
            self.print_error_message(_("Incorrect move"))
        else:
            move = [arg[0][0:2], arg[0][2:4]]

            if not self.game.isPossibleMove(move[0], move[1]):
                self.print_error_message(_("It is impossiple move"))
                return

            msg = "ok"
            if self.game.isWinMove(move[0], move[1]):
                msg = "win"
            if self.game.isDrawMove(move[0], move[1]):
                msg = "draw"

            self.game.move(move[0], move[1])
            print(self.game.get_board())

            num = self.request_num()
            self.request[num] = None
            self.write_to_server("move " + arg[0] + ":" + msg, num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                print(_(server_answer[self.request[num]]))
            if msg == "win":
                print(_("Stop game, you win!"))
            if msg == "draw":
                print(_("Stop game, draw"))

    def complete_move(self, text, line, begidx, endidx):
        """print all passible move"""
        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                for start, ends in self.game.get_possible_moves().items():
                    for end in ends:
                        complition.append(start+end)

        return [c for c in complition if c.startswith(text)]

    def do_draw(self, arg):
        """draw"""
        arg = shlex.split(arg)
        if self.game is None:
            self.print_error_message(_("You dont play now"))
        elif len(arg) > 1:
            self.print_error_message(_("More arguments"))
        elif len(arg) < 1:
            self.print_error_message(_("Not enough arguments"))
        elif not (arg[0] == "ok" or arg[0] == "not"):
            self.print_error_message(_("Incorrect argument"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("draw " + arg[0], num)
            while self.request[num] is None:
                pass
            if self.request[num]:
                if self.request[num] == "send_draw_request":
                    self.draw_request = True
                if self.request[num] == "draw":
                    self.game = None
                    self.draw_request = False
                print(_(server_answer[self.request[num]]))

    def complete_draw(self, text, line, begidx, endidx):
        """print all passible move"""
        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                complition = ['ok', 'not']
        return [c for c in complition if c.startswith(text)]

    def do_give_up(self, arg):
        """dive up"""
        arg = shlex.split(arg)
        if self.game is None:
            self.print_error_message(_("You dont play now"))
        elif len(arg) > 0:
            self.print_error_message(_("More arguments"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("give_up", num)
            while self.request[num] is None:
                pass
            if self.request[num] == "you_success_give_up":
                self.game = None
                self.draw_request = False
            print(_(server_answer[self.request[num]]))

    def do_exit(self, arg):
        """Exit program"""
        return 1

    def do_EOF(self, arg):
        """Exit program"""
        return 1

    def write_to_server(self, data, request_num):
        self.socket.send((str(request_num) + ": " + data + "\n").encode())

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
                if "start_game" in data:
                    color = int(data.split()[-1][0])
                    msg = data.split()[0]
                    color = "w" if not color else "b"
                    msg = _(server_answer[msg]).format(color)
                    self.game = Game(color)
                    board = self.game.get_board()
                    print(f"\n{msg}\n{board}\n{self.prompt}" +
                          f"{readline.get_line_buffer()}", end="", flush=True)
                elif "opponent_get_move" in data:
                    msg, move = data.split()
                    move, result = move.split(":")
                    msg = _(server_answer[msg]).format(move)
                    move = [move[0:2], move[2:4]]
                    self.game.move_from_server(move[0], move[1])
                    board = self.game.get_board()
                    if result == "win" or result == "draw":
                        self.game = None
                        self.draw_request = False
                    if result == "win":
                        result = _("Stop game, you lose =(")
                    elif result == "draw":
                        result = _("Stop game, draw")
                    else:
                        result = ""
                    if result != "":
                        print(f"\n{msg}\n{board}\n{result}\n{self.prompt}" +
                              f"{readline.get_line_buffer()}",
                              end="", flush=True)
                    else:
                        print(f"\n{msg}\n{board}\n{self.prompt}" +
                              f"{readline.get_line_buffer()}",
                              end="", flush=True)
                elif "opponent_give_up" in data:
                    self.game = None
                    self.draw_request = False
                    data = _(data)
                    print(f"\n{data}\n{self.prompt}" +
                          f"{readline.get_line_buffer()}",
                          end="", flush=True)
                elif "send_you_game_request" in data:
                    opponent_name = data.split()[-1]
                    msg = data.split()[0]
                    msg = _(server_answer[msg]).format(opponent_name)
                    print(f"\n{msg}\n{self.prompt}" +
                          f"{readline.get_line_buffer()}", end="", flush=True)
                else:
                    if "opponent_refused_draw" in data:
                        self.draw_request = False
                    if data == "draw":
                        self.game = None
                        self.draw_request = False
                    data = _(server_answer[data])
                    print(f"\n{data}\n{self.prompt}" +
                          f"{readline.get_line_buffer()}", end="", flush=True)


if __name__ == "__main__":
    chess_client().cmdloop()
