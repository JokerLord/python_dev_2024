import asyncio

CLIENTS = {}

async def cow_chat(reader, writer):
    is_registered = False
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    print(me)


async def main():
    server = await asyncio.start_server(cow_chat, "127.0.0.1", 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
