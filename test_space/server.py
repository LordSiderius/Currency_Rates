import asyncio
import websockets
import random
import json

async def echo(websocket):

    async for message in websocket:

        message = json.loads(message)

        with open('input.txt', 'r') as file:

            if message['type'] == 'heartbeat':
                if random.random() > 0.3:
                    for i in range(round(random.random()*25)):
                        message = file.readline()

                await websocket.send(message)

        await asyncio.sleep(random.random() * 5.0)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever



asyncio.run(main())