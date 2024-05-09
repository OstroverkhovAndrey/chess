
import asyncio
from user_info import UserInfo
from clients_info import ClientsInfo
from games import GamesDict
from game_history import GameHistory
import random


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
        users[user_name] = UserInfo()
        users[user_name].user_name = user_name
        await send_msg(writer, command_num, "success registre\n")
    else:
        await send_msg(writer, command_num, "not success registre, \
                such a user is already registered\n")


async def login(user_name, me, writer, command_num):
    if isOnline(me):
        await send_msg(writer, command_num, "you already login\n")
    elif user_name not in users:
        await send_msg(writer, command_num, "this user_name dont registre\n")
    elif users[user_name].isOnline:
        await send_msg(writer, command_num, "this user_name already online\n")
    else:
        clients[me].user_name = user_name
        users[user_name].isOnline = True
        users[user_name].IP = me
        await send_msg(writer, command_num, "success login\n")


async def logout(me, writer=None, command_num=None):
    if isOnline(me):
        user_name = clients[me].user_name
        users[user_name].isOnline = False
        users[user_name].isPlay = False
        users[user_name].IP = ""
        clients[me].user_name = ""
        if writer is not None and command_num is not None:
            await send_msg(writer, command_num, "success logout\n")
    else:
        if writer is not None and command_num is not None:
            await send_msg(writer, command_num, "not success logout, \
                    you dont login\n")


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
        await send_msg(writer, command_num, "you dont register\n")
    elif user_name not in users:
        await send_msg(writer, command_num, "user dont registre\n")
    elif not users[user_name].isOnline:
        await send_msg(writer, command_num, "user dont online\n")
    elif clients[me].user_name == user_name:
        await send_msg(writer, command_num, "cant play with yourself\n")
    elif users[user_name].isPlay:
        await send_msg(writer, command_num, "now user play\n")
    elif user_name in game_request and game_request[user_name] ==\
            clients[me].user_name:
        del game_request[user_name]
        users[user_name].isPlay = True
        users[clients[me].user_name].isPlay = True
        color_player1 = random.randint(0, 1)
        color_player2 = 1 - color_player1
        print("start game, player1 {} {}, player2 {} {}".format(clients[me]
              .user_name, color_player1, user_name, color_player2))
        await send_msg(writer, command_num, "start game {}\n"
                       .format(color_player1))
        await clients[users[user_name].IP].queue.put("start game {}"
                                                     .format(color_player2))
        # users[clients[me].user_name].isPlay = True
        # users[user_name].isPlay = True
        # start game
        games.add_game(clients[me].user_name, user_name)
    else:
        game_request[clients[me].user_name] = user_name
        await send_msg(writer, command_num, "send game request\n")
        await clients[users[user_name].IP].queue.put(
            "{} send you game request\n".format(clients[me].user_name))


async def move_command(me, writer, move, command_num):
    if not users[clients[me].user_name].isPlay:
        await send_msg(writer, command_num, "you dont play now\n")
        return
    opponent = games[clients[me].user_name].get_opponent(clients[me].user_name)
    if games[clients[me].user_name].get_draw_request() == clients[me].user_name:
        print("Error with draw request!")
    if not games[clients[me].user_name].get_draw_request() is None:
        games[clients[me].user_name].remove_draw_request()
        await clients[users[opponent].IP].queue.put("opponent refused a draw\n")

    games[clients[me].user_name].move(clients[me].user_name, move)
    await send_msg(writer, command_num, "you get move\n")
    await clients[users[opponent].IP].queue.put(
        "opponent get move {}".format(move))
    if move.endswith("win") or move.endswith("draw"):
        print("end game ", move.split(":")[1])
        users[clients[me].user_name].isPlay = False
        users[opponent].isPlay = False
        game_story = games[clients[me].user_name].get_game_story()
        games.stop_game(clients[me].user_name, opponent)
        game_result = "draw"
        if move.endswith("win"):
            game_result = users[clients[me].user_name]
        game_history.add_game(clients[me].user_name, opponent,
                              game_result, game_story)


async def draw(me, writer, command_num, msg):
    if not users[clients[me].user_name].isPlay:
        await send_msg(writer, command_num, "you dont play now\n")
        return
    game = games[clients[me].user_name]
    opponent = game.get_opponent(clients[me].user_name)
    if game.get_draw_request() is None:
        if msg == "ok":
            game.set_draw_request(clients[me].user_name)
            await send_msg(writer, command_num, "send draw request\n")
            await clients[users[opponent].IP].queue.put(
                "opponent send you draw request\n")
        elif msg == "not":
            await send_msg(writer, command_num,
                           "opponent dont send draw request\n")
    else:
        if game.get_draw_request() == clients[me].user_name and msg == "ok":
            await send_msg(writer, command_num, "send draw request\n")
        elif game.get_draw_request() == clients[me].user_name and msg == "not":
            await send_msg(writer, command_num,
                           "you dont delete draw request\n")
        elif msg == "not":
            await send_msg(writer, command_num, "you refused a draw\n")
            await clients[users[opponent].IP].queue.put(
                "opponent refused a draw\n")
            game.remove_draw_request()
        elif msg == "ok":
            print("end game draw")
            await send_msg(writer, command_num, "draw\n")
            await clients[users[opponent].IP].queue.put("draw\n")
            game.move(clients[me].user_name, "draw")
            users[clients[me].user_name].isPlay = False
            users[opponent].isPlay = False
            game_story = game.get_game_story()
            games.stop_game(clients[me].user_name, opponent)
            game_result = "draw"
            game_history.add_game(clients[me].user_name, opponent,
                                  game_result, game_story)


async def give_up(me, writer, command_num):
    print("end game draw")
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
    asyncio.run(main())
