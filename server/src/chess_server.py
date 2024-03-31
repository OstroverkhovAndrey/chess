
import asyncio
from user_info import UserInfo
from clients_info import ClientsInfo

clients = {} # ip to clients_info
users = {} # user_name to user_info, need load from memory
game_request = {} # player1 -> player2

games = {}

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

async def chess_server(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = ClientsInfo()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:

                command = q.result().decode().strip().split()
                print(me, command)

                match command:
                    case ["registre", user_name]:
                        if user_name not in users:
                            users[user_name] = UserInfo()
                            users[user_name].user_name = user_name
                            await send_msg(writer, 0, "success registre\n")
                        else:
                            await send_msg(writer, 0, "not success registre, such a user is already registered\n")
                    case ["login", user_name]:
                        # need more if
                        if not isOnline(me) and user_name in users and not users[user_name].isOnline:
                            clients[me].user_name = user_name
                            users[user_name].isOnline = True
                            users[user_name].IP = me
                            await send_msg(writer, 0, "success login\n")
                        else:
                            await send_msg(writer, 0, "not success login, such a user is not registered\n")
                    case ["logout"]:
                        if isOnline(me):
                            user_name = clients[me].user_name
                            users[user_name].isOnline = False
                            users[user_name].IP = ""
                            del clients[me].user_name
                            await send_msg(writer, 0, "success logout\n")
                        else:
                            await send_msg(writer, 0, "not success logout, you dont login\n")
                    case ["users"]:
                        online_users = [user.user_name for _, user in clients.items() if user.user_name != ""]
                        online_users = " ".join(online_users)
                        writer.write(online_users.encode())
                        await writer.drain()
                    case ["play", user_name]:
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
                        elif user_name in game_request and game_request[user_name] == clients[me].user_name:
                            del game_request[user_name]
                            users[user_name].isPlay = True
                            users[clients[me].user_name].isPlay = True
                            print("start game, player1 {}, player2 {}".format(clients[me].user_name, user_name))
                            # start game
                        else:
                            game_request[clients[me].user_name] = user_name
                            await send_msg(writer, 0, "send game request\n")
                            
                    case ["statistic", user_name]:
                        pass
                    case ["chat"]:
                        pass
                    case ["move", move]:
                        pass
                    case ["draw"]:
                        pass
                    case ["give_up"]:
                        pass
                send = asyncio.create_task(reader.readline())
            elif q is receive:
                receive = asyncio.create_task(clients[me].queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
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

