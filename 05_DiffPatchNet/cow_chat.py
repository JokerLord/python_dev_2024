import asyncio

CLIENTS = {}


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
                print(q.result())
    
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