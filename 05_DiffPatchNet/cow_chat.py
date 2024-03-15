import asyncio
import shlex
import cowsay

CLIENTS = {}


async def async_write(writer, text):
    writer.write(f"{text}\n".encode())
    await writer.drain()


async def cow_chat(reader, writer):
    is_registered = False
    client_id = "{}:{}".format(*writer.get_extra_info("peername"))

    send = asyncio.create_task(reader.readline())  # when client enter message
    receive = None  # no receive yet, because client is not registered
    while not reader.at_eof():
        if receive is None:
            done, pending = await asyncio.wait(
                [send], return_when=asyncio.FIRST_COMPLETED
            )
        else:
            done, pending = await asyncio.wait(
                [send, receive], return_when=asyncio.FIRST_COMPLETED
            )
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                args = shlex.split(q.result().decode().strip())
                if not args:
                    continue
                if args[0] == "who":
                    await async_write(
                        writer, f"Registered users: {' '.join(CLIENTS.keys())}"
                    )
                elif args[0] == "cows":
                    available_cows = [
                        cow for cow in cowsay.list_cows() if cow not in CLIENTS
                    ]
                    await async_write(
                        writer, f"Cows available: {' '.join(available_cows)}"
                    )
                elif args[0] == "login":
                    if is_registered:
                        await async_write(
                            writer, "Failed to login. You are already registered"
                        )
                    elif len(args) < 2:
                        await async_write(
                            writer, "Failed to login. Login name wasn't passed"
                        )
                    elif len(args) > 2:
                        await async_write(
                            writer, "Failed to login. Too many parameters"
                        )
                    else:
                        available_cows = [
                            cow for cow in cowsay.list_cows() if cow not in CLIENTS
                        ]
                        if args[1] in available_cows:
                            me = args[1]
                            CLIENTS[me] = asyncio.Queue()
                            receive = asyncio.create_task(CLIENTS[me].get())
                            is_registered = True
                            await async_write(writer, "Login success")
                        else:
                            await async_write(writer, "Login not awailable")
                elif args[0] == "say":
                    if not is_registered:
                        await async_write(writer, "You are not registered")
                    elif len(args) != 3:
                        await async_write(writer, "Invalid command 'say' syntax")
                    else:
                        if args[1] in CLIENTS:
                            await CLIENTS[args[1]].put(cowsay.cowsay(args[2], cow=me))
                        else:
                            await async_write(writer, "No such user online")
                elif args[0] == "yield":
                    if not is_registered:
                        await async_write(writer, "You are not registered")
                    elif len(args) != 2:
                        await async_write(writer, "Invalid command 'yield' syntax")
                    else:
                        for client in CLIENTS:
                            if client != me:
                                await CLIENTS[client].put(
                                    cowsay.cowsay(args[1], cow=me)
                                )
            if q is receive:
                receive = asyncio.create_task(CLIENTS[me].get())
                await async_write(writer, q.result())
    send.cancel()
    if receive:
        receive.cancel()
    del CLIENTS[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(cow_chat, "127.0.0.1", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
