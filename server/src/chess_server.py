
import asyncio

clients = {}

async def chess_server(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                comand = q.result().decode().strip().split()
                print(me, comand)

                match comand:
                    case ["registre", user_name]:
                        pass
                    case ["login", user_name]:
                        pass
                    case ["logout"]:
                        pass
                    case ["users"]:
                        pass
                    case ["play", user_name]:
                        pass
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
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
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

