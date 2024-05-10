
import asyncio
from user_info import UserInfo
from clients_info import ClientsInfo
from games import GamesDict
from game_history import GameHistory
import random
from dump_load import dump_user_info, load_user_info
from dump_load import dump_game_history, load_game_history


clients = {}  # ip to clients_info
users = {}  # user_name to user_info, need load from memory
game_request = {}  # player1 -> player2
games = GamesDict()
game_history = GameHistory()

"""
command ids
0: simple message for client or user
"""


def isOnline(me):
    return me in clients and clients[me].user_name != ""


async def send_msg(writer, ids, msg):
    msg = str(ids) + ":" + msg
    writer.write(msg.encode())
    await writer.drain()


def get_msg_num(msg):
    num = msg.strip().split(":")[0]
    if num.isnumeric():
        msg = msg[len(num)+1:].strip()
        return int(num), msg
    else:
        return 0, msg


async def registre(user_name, writer, command_num):
    if user_name not in users:
        users[user_name] = UserInfo(user_name)
        dump_user_info(users)
        await send_msg(writer, command_num, "registre_ok")
    else:
        await send_msg(writer, command_num, "registre_not")


async def login(user_name, me, writer, command_num):
    if isOnline(me):
        await send_msg(writer, command_num, "already_login")
    elif user_name not in users:
        await send_msg(writer, command_num, "login_dont_registre")
    elif users[user_name].isOnline:
        await send_msg(writer, command_num, "login_already_online")
    else:
        clients[me].user_name = user_name
        users[user_name].isOnline = True
        users[user_name].IP = me
        await send_msg(writer, command_num, "success_login")


async def logout(me, writer=None, command_num=None):
    if isOnline(me):
        user_name = clients[me].user_name
        if users[user_name].isOnline and users[user_name].isPlay:
            # you lose
            print("end game logout")
            game = games[clients[me].user_name]
            opponent = game.get_opponent(clients[me].user_name)
            if writer is not None and command_num is not None:
                await send_msg(writer, 0, "success_logout_give_up")
            await clients[users[opponent].IP].queue.put("opponent_give_up")
            game.move(clients[me].user_name, "give_up")
            users[clients[me].user_name].isPlay = False
            users[opponent].isPlay = False
            game_story = game.get_game_story()
            games.stop_game(clients[me].user_name, opponent)
            game_result = opponent
            game_history.add_game(clients[me].user_name, opponent,
                                  game_result, game_story)
        users[user_name].isOnline = False
        users[user_name].isPlay = False
        users[user_name].IP = ""
        clients[me].user_name = ""
        if writer is not None and command_num is not None:
            await send_msg(writer, command_num, "success_logout")
    else:
        if writer is not None and command_num is not None:
            await send_msg(writer, command_num, "logout_not")


async def get_offline_users(writer, command_num):
    offline_users = [name for name, info in users.items()
                     if not info.isOnline]
    offline_users = " ".join(offline_users) + "\n"
    await send_msg(writer, command_num, offline_users)


async def get_online_users(writer, command_num):
    online_users = [user.user_name for _, user in clients.items()
                    if user.user_name != ""]
    online_users = " ".join(online_users) + "\n"
    await send_msg(writer, command_num, online_users)


async def get_game_request(me, writer, command_num):
    game_request_from_me = [user2 for user1, user2 in game_request.items()
                            if user1 == clients[me].user_name]
    game_request_from_me = "from me: " + " ".join(game_request_from_me) + "\n"
    game_request_for_me = [user1 for user1, user2 in game_request.items()
                           if user2 == clients[me].user_name]
    game_request_for_me = "for me: " + " ".join(game_request_for_me) + "\n"
    await send_msg(writer, command_num, game_request_from_me +
                   game_request_for_me)


async def remove_game_request(me, writer, command_num):
    user_name = clients[me].user_name
    if user_name in game_request:
        del game_request[user_name]
        ans = "success remove\n"
    else:
        ans = "not found you game request\n"
    await send_msg(writer, command_num, ans)


async def get_statistic(me, writer, command_num, user_name=""):
    if user_name == "":
        user_name = clients[me].user_name
    statistic = game_history.get_statistic_for_user(user_name)
    statistic = "statistic for {}\nwin: {}\ndraw: {}\ndefeat: {}\n".format(
                 user_name, *statistic)
    await send_msg(writer, command_num, statistic)


async def play(user_name, me, writer, command_num):
    if not isOnline(me):
        await send_msg(writer, command_num, "you_dont_register")
    elif user_name not in users:
        await send_msg(writer, command_num, "opponent_dont_registre")
    elif not users[user_name].isOnline:
        await send_msg(writer, command_num, "opponent_dont_online")
    elif clients[me].user_name == user_name:
        await send_msg(writer, command_num, "cant_play_with_yourself")
    elif users[user_name].isPlay:
        await send_msg(writer, command_num, "now_opponent_play")
    elif users[clients[me].user_name].isPlay:
        await send_msg(writer, command_num, "now_you_play")
    elif user_name in game_request and game_request[user_name] ==\
            clients[me].user_name:
        del game_request[user_name]
        users[user_name].isPlay = True
        users[clients[me].user_name].isPlay = True
        color_player1 = random.randint(0, 1)
        color_player2 = 1 - color_player1
        print("start game, player1 {} {}, player2 {} {}".format(clients[me]
              .user_name, color_player1, user_name, color_player2))
        await send_msg(writer, command_num, "start_game " + str(color_player1))
        await clients[users[user_name].IP].queue.put("start_game " + str(color_player2))
        games.add_game(clients[me].user_name, user_name)
    else:
        game_request[clients[me].user_name] = user_name
        await send_msg(writer, command_num, "send_game_request")
        await clients[users[user_name].IP].queue.put(
            "send_you_game_request " + clients[me].user_name)


async def move_command(me, writer, move, command_num):
    if clients[me].user_name == "":
        await send_msg(writer, command_num, "move_not_dont_login")
        return
    if not users[clients[me].user_name].isPlay:
        await send_msg(writer, command_num, "move_not_you_dont_play_now")
        return
    opponent = games[clients[me].user_name].get_opponent(clients[me].user_name)
    if games[clients[me].user_name].get_draw_request() == clients[me].user_name:
        print("Error with draw request!")
    if not games[clients[me].user_name].get_draw_request() is None:
        games[clients[me].user_name].remove_draw_request()
        await clients[users[opponent].IP].queue.put("move_opponent_refused_draw")

    games[clients[me].user_name].move(clients[me].user_name, move)
    await send_msg(writer, command_num, "you_get_move")
    await clients[users[opponent].IP].queue.put("opponent_get_move " + move)
    if move.endswith("win") or move.endswith("draw"):
        print("end game ", move.split(":")[1])
        users[clients[me].user_name].isPlay = False
        users[opponent].isPlay = False
        game_story = games[clients[me].user_name].get_game_story()
        games.stop_game(clients[me].user_name, opponent)
        game_result = "draw"
        if move.endswith("win"):
            game_result = clients[me].user_name
        game_history.add_game(clients[me].user_name, opponent,
                              game_result, game_story)
        dump_game_history(game_history)


async def draw(me, writer, command_num, msg):
    if clients[me].user_name == "":
        await send_msg(writer, command_num, "dont_login")
        return
    if not users[clients[me].user_name].isPlay:
        await send_msg(writer, command_num, "you_dont_play_now")
        return
    game = games[clients[me].user_name]
    opponent = game.get_opponent(clients[me].user_name)
    if game.get_draw_request() is None:
        if msg == "ok":
            game.set_draw_request(clients[me].user_name)
            await send_msg(writer, command_num, "send_draw_request")
            await clients[users[opponent].IP].queue.put(
                "opponent_send_you_draw_request")
        elif msg == "not":
            await send_msg(writer, command_num,
                           "opponent_dont_send_draw_request")
    else:
        if game.get_draw_request() == clients[me].user_name and msg == "ok":
            await send_msg(writer, command_num, "send_draw_request")
        elif game.get_draw_request() == clients[me].user_name and msg == "not":
            await send_msg(writer, command_num,
                           "you_cant_delete_draw_request")
        elif msg == "not":
            await send_msg(writer, command_num, "you_refused_draw")
            await clients[users[opponent].IP].queue.put(
                "opponent_refused_draw")
            game.remove_draw_request()
        elif msg == "ok":
            print("end game draw")
            await send_msg(writer, command_num, "draw")
            await clients[users[opponent].IP].queue.put("draw")
            game.move(clients[me].user_name, "draw")
            users[clients[me].user_name].isPlay = False
            users[opponent].isPlay = False
            game_story = game.get_game_story()
            games.stop_game(clients[me].user_name, opponent)
            game_result = "draw"
            game_history.add_game(clients[me].user_name, opponent,
                                  game_result, game_story)
            dump_game_history(game_history)


async def give_up(me, writer, command_num):
    if clients[me].user_name == "":
        await send_msg(writer, command_num, "you dont login now\n")
        return
    if not users[clients[me].user_name].isPlay:
        await send_msg(writer, command_num, "you dont play now\n")
        return
    print("end game give_up")
    game = games[clients[me].user_name]
    opponent = game.get_opponent(clients[me].user_name)
    await send_msg(writer, command_num, "yoe success give up\n")
    await clients[users[opponent].IP].queue.put("opponent give up\n")
    game.move(clients[me].user_name, "give_up")
    users[clients[me].user_name].isPlay = False
    users[opponent].isPlay = False
    game_story = game.get_game_story()
    games.stop_game(clients[me].user_name, opponent)
    game_result = opponent
    game_history.add_game(clients[me].user_name, opponent,
                          game_result, game_story)
    dump_game_history(game_history)


async def chess_server(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = ClientsInfo()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive],
                                           return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:

                command_num, command = get_msg_num(q.result().decode())
                command = command.strip().split()
                print(me, command_num, command)

                match command:
                    case ["registre", user_name]:
                        await registre(user_name, writer, command_num)
                    case ["login", user_name]:
                        await login(user_name, me, writer, command_num)
                    case ["logout"]:
                        await logout(me, writer, command_num)
                    case ["offline_users"]:
                        await get_offline_users(writer, command_num)
                    case ["online_users"]:
                        await get_online_users(writer, command_num)
                    case ["game_request"]:
                        await get_game_request(me, writer, command_num)
                    case ["play", user_name]:
                        await play(user_name, me, writer, command_num)
                    case ["remove_game_request"]:
                        await remove_game_request(me, writer, command_num)
                    case ["statistic"]:
                        await get_statistic(me, writer, command_num)
                    case ["statistic", user_name]:
                        await get_statistic(me, writer, command_num, user_name)
                    case ["chat"]:
                        pass
                    case ["move", move]:
                        print(move)
                        await move_command(me, writer, move, command_num)
                    case ["draw", msg]:
                        await draw(me, writer, command_num, msg)
                    case ["give_up"]:
                        await give_up(me, writer, command_num)
                send = asyncio.create_task(reader.readline())
            elif q is receive:
                receive = asyncio.create_task(clients[me].queue.get())
                await send_msg(writer, 0, q.result())
                # writer.write(f"{q.result()}\n".encode())
                # await writer.drain()
    await logout(me)
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chess_server, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    users = load_user_info()
    game_history = load_game_history()
    asyncio.run(main())
