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

    send.cancel()
    if receive:
        receive.cancel()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(cow_chat, "127.0.0.1", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
