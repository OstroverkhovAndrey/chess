
import asyncio
from user_info import UserInfo
from clients_info import ClientsInfo

clients = {} # ip to clients_info
users = {} # user_name to user_info, need load from memory
game_request = {} # player1 -> player2

games = {}

def isOnline(me):
    return me in clients and clients[me].user_name != ""

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

                comand = q.result().decode().strip().split()
                print(me, comand)

                match comand:
                    case ["registre", user_name]:
                        if user_name not in users:
                            users[user_name] = UserInfo()
                            users[user_name].user_name = user_name
                            #say success registre
                        else:
                            #say not success registre
                            pass
                    case ["login", user_name]:
                        if not isOnline(me) and user_name in users:
                            clients[me].user_name = user_name
                            users[user_name].isOnline = True
                            users[user_name].IP = me
                            # say success login
                        else:
                            # say user not registre
                            pass
                    case ["logout"]:
                        if isOnline(me):
                            user_name = clients[me].user_name
                            users[user_name].isOnline = False
                            users[user_name].IP = ""
                            del clients[me].user_name
                            # say success logout
                        else:
                            #say you dont login
                            pass
                    case ["users"]:
                        online_users = [user.user_name for _, user in clients.items() if user.user_name != ""]
                        online_users = " ".join(online_users)
                        writer.write(online_users.encode())
                        await writer.drain()
                    case ["play", user_name]:
                        if not isOnline(me):
                            print("you dont register")
                        elif user_name not in users:
                            print("user dont registre")
                        elif not users[user_name].isOnline:
                            print("user dont online")
                        elif clients[me].user_name == user_name:
                            print("cant play with yourself")
                        elif users[user_name].isPlay:
                            print("now user play")
                        elif user_name in game_request and game_request[user_name] == clients[me].user_name:
                            del game_request[user_name]
                            users[user_name].isPlay = True
                            users[clients[me].user_name].isPlay = True
                            print("start game, player1 {}, player2 {}".format(clients[me].user_name, user_name))
                            # start game
                        else:
                            game_request[clients[me].user_name] = user_name
                            print("send game request")
                            
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

