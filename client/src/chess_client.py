
"""A module implementing a client for playing chess."""

import cmd
import threading
import readline
import socket
import shlex
from chess_game import Game
from internationalization import _
from server_answer import server_answer
import locale


class chess_client(cmd.Cmd):
    """
    Class implementing a chess game client.

    Methods
    -------
    request_num(self) -> int
        Returns the next request number for the server
    complition_num(self) -> int
        Returns the next complition request number for the server
    print_error_message(self, error: str = "") -> None
        Print message for user
    do_registre(self, arg: str) -> None
        Registre form chess server
    do_login(self, arg: str) -> None
        Login form chess server
    complete_login(self, text: str, line: str, begidx: int, endidx: int) -> list
        Complete login command
    do_logout(self, arg: str) -> None
        Logout form chess server and give up if user is playing
    do_get_users(self, arg: str) -> None
        Print name online users from server
    do_get_game_request(self, arg: str) -> None
        Print game request from/for current player
    do_remove_game_request(self, arg: str) -> None
        Remove game request from current player
    do_get_statistic(self, arg: str) -> None
        Print statistic for current player or other player
    do_play(self, arg: str) -> None
        Send play request or accept play request
    complete_play(self, text: str, line: str, begidx: int, endidx: int) -> list
        Complete play command
    do_move(self, arg: str) -> None
        Make a move in chess play
    complete_move(self, text: str, line: str, begidx: int, endidx: int) -> list
        Complete move command
    do_draw(self, arg) -> None
        Send draw request or agree with draw
    complete_draw(self, text: str, line: str, begidx: itn, endidx: int) -> list
        Complete draw command
    do_give_up(self, arg: str) -> None
        Give up in current game
    do_exit(self, arg: str) -> None
        Exit program
    do_EOF(self, arg: str) -> None
        Exit program
    write_to_server(self, data: str, request_num: int) -> None
        Send request to server
    read_from_server(self) -> None
        Accepts messages from the server
    """

    prompt = "chess >> "

    def __init__(self) -> None:
        """Init chess_client."""
        super().__init__()
        self.socket = socket.socket()
        self.socket.connect(("0.0.0.0", 1337))
        self.timer = threading.Thread(target=self.read_from_server, args=())
        self.timer.start()
        self.rn = 1
        self.cn = 2
        self.request = {}
        self.complet = {}
        self.name = ""
        self.game = None
        self.draw_request = False

    def request_num(self) -> int:
        """
        Returns the next request number for the server.

        Returns
        -------
        int
            Next request nember
        """
        self.rn += 2
        return self.rn

    def complet_num(self) -> int:
        """
        Returns the next complition request number for the server.

        Returns
        -------
        int
            Next complition request nember
        """
        self.cn += 2
        return self.cn

    def wait_request_ans(self, num: int) -> None:
        """
        Waiting for the response from the server to be received.

        Parameters
        ----------
        num : int
            Request num
        """
        while self.request[num] is None:
            pass

    def wait_complet_ans(self, num: int) -> None:
        """
        Waiting for the response from the server to be received.

        Parameters
        ----------
        num : int
            Request num
        """
        while self.complet[num] is None:
            pass

    def do_set_language(self, arg: str) -> None:
        """
        Set text interface language.

        Parameters
        ----------
        arg : str
            Contains the desired language of the text interface. Now: en, ru
        """
        arg = shlex.split(arg)
        if len(arg) > 1:
            print(_("More arguments"))
        elif len(arg) < 1:
            print(_("Not enough arguments"))
        elif arg[0] != "en" and arg[0] != "ru":
            print(_("This language is currently not supported"))
        elif arg[0] == "en":
            locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))
            print(_("Set language"))
        elif arg[0] == "ru":
            locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))
            print(_("Set language"))

    def complete_set_language(
            self, text: str, line: str, begidx: int, endidx: int) -> list:
        """
        Complete set language command.

        Parameters
        ----------
        text : str
            Prefix
        line : str
            All line
        begidx : int
            Prefix start
        endidx : int
            Prefix end

        Returns
        -------
        list
            [en | ru]
        """
        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                complition = ['en', 'ru']
        return [c for c in complition if c.startswith(text)]

    def do_registre(self, arg: str) -> None:
        """
        Registre form chess server.

        Parameters
        ----------
        arg : str
            Must contain the name of the new user
        """
        arg = shlex.split(arg)
        if len(arg) > 1:
            print(_("More arguments"))
        elif len(arg) < 1:
            print(_("Not enough arguments"))
        elif not arg[0].isalnum():
            print(_("Incorrect name"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("registre " + arg[0], num)
            self.wait_request_ans(num)
            if self.request[num]:
                print(_(server_answer[self.request[num]]))

    def do_login(self, arg: str) -> None:
        """
        Login form chess server.

        Parameters
        ----------
        arg : str
            Must contain the name of the login user
        """
        arg = shlex.split(arg)
        if len(arg) > 1:
            print(_("More arguments"))
        elif len(arg) < 1:
            print(_("Not enough arguments"))
        elif not arg[0].isalnum():
            print(_("Incorrect name"))
        elif self.name != "":
            print(_("You already login"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("login " + arg[0], num)
            self.wait_request_ans(num)
            if self.request[num]:
                if self.request[num] == "success_login":
                    self.name = arg[0]
                print(_(server_answer[self.request[num]]))

    def complete_login(
            self, text: str, line: str, begidx: int, endidx: int) -> list:
        """
        Complete login command.

        Parameters
        ----------
        text : str
            Prefix
        line : str
            All line
        begidx : int
            Prefix start
        endidx : int
            Prefix end

        Returns
        -------
        list
            Current ofline users in server
        """
        num = self.complet_num()
        self.complet[num] = None
        self.write_to_server("offline_users", num)

        self.wait_complet_ans(num)

        words = (line[:endidx] + ".").split()
        complet = []
        match len(words):
            case 2:
                complet = self.complet[num].split()
        return [c for c in complet if c.startswith(text)]

    def do_logout(self, arg: str) -> None:
        """
        Logout form chess server and give up if user is playing.

        Parameters
        ----------
        arg : str
            Should be empty
        """
        arg = shlex.split(arg)
        if len(arg) > 0:
            print(_("More arguments"))
        elif self.name == "":
            print(_("You dont login"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("logout", num)
            self.wait_request_ans(num)
            if self.request[num]:
                if self.request[num] == "success_logout":
                    self.name = ""
                    self.game = None
                    self.draw_request = False
                print(_(server_answer[self.request[num]]))

    def do_get_users(self, arg: str) -> None:
        """
        Print name online users from server.

        Parameters
        ----------
        arg : str
            Should be empty
        """
        arg = shlex.split(arg)
        if len(arg) > 0:
            print(_("More arguments"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("online_users", num)
            self.wait_request_ans(num)
            if self.request[num]:
                print(self.request[num])

    def do_get_game_request(self, arg: str) -> None:
        """
        Print game request from/for current player.

        Parameters
        ----------
        arg : str
            Should be empty
        """
        arg = shlex.split(arg)
        if len(arg) > 0:
            print(_("More arguments"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("game_request", num)
            self.wait_request_ans(num)
            if self.request[num]:
                msg, from_me, for_me = self.request[num].split(".")
                print(_(server_answer[msg]).format(from_me, for_me))

    def do_remove_game_request(self, arg: str) -> None:
        """
        Remove game request from current player.

        Parameters
        ----------
        arg : str
            Should be empty
        """
        if len(arg) > 0:
            print(_("More arguments"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("remove_game_request", num)
            self.wait_request_ans(num)
            if self.request[num]:
                print(_(server_answer[self.request[num]]))

    def do_get_statistic(self, arg: str) -> None:
        """
        Print statistic for current player or other player.

        Parameters
        ----------
        arg : str
            May contain the user's name
        """
        arg = shlex.split(arg)
        if len(arg) > 1:
            print(_("More arguments"))
        else:
            user = ""
            if len(arg) == 1 and arg[0].isalnum():
                user = arg[0]
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("statistic " + user, num)
            self.wait_request_ans(num)
            if self.request[num]:
                msg, user_name, win, draw, defeat = self.request[num].split(".")
                print(_(server_answer[msg]).format(
                    user_name, win, draw, defeat))

    def do_play(self, arg: str) -> None:
        """
        Send play request or accept play request.

        Parameters
        ----------
        arg : str
            Must contain the opponent name
        """
        arg = shlex.split(arg)
        if len(arg) > 1:
            print(_("More arguments"))
        elif len(arg) < 1:
            print(_("Not enough arguments"))
        elif not arg[0].isalnum():
            print(_("Incorrect name"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("play " + arg[0], num)
            self.wait_request_ans(num)
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

    def complete_play(
            self, text: str, line: str, begidx: int, endidx: int) -> list:
        """
        Complete play command.

        Parameters
        ----------
        text : str
            Prefix
        line : str
            All line
        begidx : int
            Prefix start
        endidx : int
            Prefix end

        Returns
        -------
        list
            Current online users in server
        """
        num = self.complet_num()
        self.complet[num] = None
        self.write_to_server("online_users", num)

        self.wait_complet_ans(num)

        words = (line[:endidx] + ".").split()
        complet = []
        match len(words):
            case 2:
                complet = self.complet[num].split()
        return [c for c in complet if c.startswith(text) and c != self.name]

    def do_move(self, arg: str) -> None:
        """
        Make a move in chess play.

        Parameters
        ----------
        arg : str
            Must contain move. Old field and new field, example e2e4.
            Castling is recorded as the movement of the king, example e1g1.
        """
        arg = shlex.split(arg)
        if self.game is None:
            print(_("You dont play now"))
        elif not self.game.isMyMove():
            print(_("Now not you move"))
        elif len(arg) > 1:
            print(_("More arguments"))
        elif len(arg) < 1:
            print(_("Not enough arguments"))
        elif self.draw_request:
            print(_("You send draw request"))
        elif len(arg[0]) != 4:
            print(_("Incorrect move"))
        else:
            move = [arg[0][0:2], arg[0][2:4]]

            if not self.game.isPossibleMove(move[0], move[1]):
                print(_("It is impossiple move"))
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
            self.wait_request_ans(num)
            if self.request[num]:
                print(_(server_answer[self.request[num]]))
            if msg != "ok":
                self.draw_request = False
                self.game = None
            if msg == "win":
                print(_("Stop game, you win!"))
            if msg == "draw":
                print(_("Stop game, draw"))

    def complete_move(
            self, text: str, line: str, begidx: int, endidx: int) -> list:
        """
        Complete move command.

        Parameters
        ----------
        text : str
            Prefix
        line : str
            All line
        begidx : int
            Prefix start
        endidx : int
            Prefix end

        Returns
        -------
        list
            Possible moves with the current start
        """
        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                for start, ends in self.game.get_possible_moves().items():
                    for end in ends:
                        complition.append(start+end)

        return [c for c in complition if c.startswith(text)]

    def do_draw(self, arg: str) -> None:
        """
        Send draw request or agree with draw.

        Parameters
        ----------
        arg : str
            Must contain ok or not. ok if you want to send draw request
            or you want to agree with draw. not if you don`t want to draw.
        """
        arg = shlex.split(arg)
        if self.game is None:
            print(_("You dont play now"))
        elif len(arg) > 1:
            print(_("More arguments"))
        elif len(arg) < 1:
            print(_("Not enough arguments"))
        elif not (arg[0] == "ok" or arg[0] == "not"):
            print(_("Incorrect argument"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("draw " + arg[0], num)
            self.wait_request_ans(num)
            if self.request[num]:
                if self.request[num] == "send_draw_request":
                    self.draw_request = True
                if self.request[num] == "draw":
                    self.game = None
                    self.draw_request = False
                print(_(server_answer[self.request[num]]))

    def complete_draw(
            self, text: str, line: str, begidx: int, endidx: int) -> list:
        """
        Complete draw command.

        Parameters
        ----------
        text : str
            Prefix
        line : str
            All line
        begidx : int
            Prefix start
        endidx : int
            Prefix end

        Returns
        -------
        list
            [ok | not]
        """
        words = (line[:endidx] + ".").split()
        complition = []
        match len(words):
            case 2:
                complition = ['ok', 'not']
        return [c for c in complition if c.startswith(text)]

    def do_give_up(self, arg: str) -> None:
        """
        Give up in current game.

        Parameters
        ----------
        arg : str
            Should be empty
        """
        arg = shlex.split(arg)
        if self.game is None:
            print(_("You dont play now"))
        elif len(arg) > 0:
            print(_("More arguments"))
        else:
            num = self.request_num()
            self.request[num] = None
            self.write_to_server("give_up", num)
            self.wait_request_ans(num)
            if self.request[num] == "you_success_give_up":
                self.game = None
                self.draw_request = False
            print(_(server_answer[self.request[num]]))

    def do_exit(self, arg: str) -> None:
        """Exit program."""
        return 1

    def do_EOF(self, arg: str) -> None:
        """Exit program."""
        return 1

    def write_to_server(self, data: str, request_num: int) -> None:
        """
        Send request to server.

        Parameters
        ----------
        data : str
            Request to server
        request_num : int
            Number of request
        """
        self.socket.send((str(request_num) + ": " + data + "\n").encode())

    def read_from_server(self) -> None:
        """
        Accepts messages from the server.

        If the received message is a response to the request, it puts
        the response in the dictionary with the corresponding key
        to the request number, otherwise it displays the message on the screen
        """
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            data = self.socket.recv(1024).decode()
            data_num = data.split(":")[0]
            data = data[len(data_num)+1:].strip()
            data_num = int(data_num)
            if data_num in self.complet and\
                    self.complet[data_num] is None:
                self.complet[data_num] = data
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
