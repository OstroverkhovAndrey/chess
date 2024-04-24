
import asyncio
from user_info import UserInfo
from clients_info import ClientsInfo
from games import GamesDict


clients = {}  # ip to clients_info
users = {}  # user_name to user_info, need load from memory
game_request = {}  # player1 -> player2
games = GamesDict()

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
        users[user_name].IP = ""
        clients[me].user_name = ""
        if writer is not None and command_num is not None:
            await send_msg(writer, command_num, "success logout\n")
    else:
        if writer is not None and command_num is not None:
            await send_msg(writer, command_num, "not success logout, \
                    you dont login\n")


async def get_users(writer, command_num):
    online_users = [user.user_name for _, user in clients.items()
                    if user.user_name != ""]
    online_users = " ".join(online_users) + "\n"
    await send_msg(writer, command_num, online_users)


async def play(user_name, me, writer):
    if not isOnline(me):
        await send_msg(writer, 0, "you dont register\n")
    elif user_name not in users:
        await send_msg(writer, 0, "user dont registre\n")
    elif not users[user_name].isOnline:
        await send_msg(writer, 0, "user dont online\n")
    elif clients[me].user_name == user_name:
        await send_msg(writer, 0, "cant play with yourself\n")
    elif users[user_name].isPlay:
        await send_msg(writer, 0, "now user play\n")
    elif user_name in game_request and game_request[user_name] ==\
            clients[me].user_name:
        del game_request[user_name]
        users[user_name].isPlay = True
        users[clients[me].user_name].isPlay = True
        print("start game, player1 {}, player2 {}".format(clients[me]
              .user_name, user_name))
        await send_msg(writer, 0, "start game\n")
        await clients[users[user_name].IP].queue.put("start game")
        # start game
        games.add_game(clients[me].user_name, user_name)
    else:
        game_request[clients[me].user_name] = user_name
        await send_msg(writer, 0, "send game request\n")


async def move_command(me, move, msg):
    games[clients[me].user_name].move(clients[me].user_name, move, msg[0])


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
                    case ["users"]:
                        await get_users(writer, command_num)
                    case ["play", user_name]:
                        await play(user_name, me, writer)
                    case ["statistic", user_name]:
                        pass
                    case ["chat"]:
                        pass
                    case ["move", move, *msg]:
                        await move_command(me, move, msg)
                    case ["draw"]:
                        pass
                    case ["give_up"]:
                        pass
                send = asyncio.create_task(reader.readline())
            elif q is receive:
                receive = asyncio.create_task(clients[me].queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
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
