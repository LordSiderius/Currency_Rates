import asyncio
import websockets
import random
import json

async def echo(websocket):

    async for message in websocket:

        message = json.loads(message)
        # path = 'test_messages/invalid_date_currency.txt'
        path = 'test_messages/mixed_messages.txt'
        print(message)

        with open(path, 'r') as file:
            text = file.readlines()
            size = len(text)

            if message['type'] == 'heartbeat':
                message = json.dumps(message)
                if random.random() > 0.3:
                    message = text[random.randint(0, size - 1)]
                await asyncio.wait_for(websocket.send(message), timeout=0.2)

        # simulation of server timeout
        await asyncio.sleep(random.random() * 2.0)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever



asyncio.run(main())