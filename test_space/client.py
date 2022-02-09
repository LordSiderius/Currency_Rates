#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            await websocket.send("Hello world!")
            message = await websocket.recv()
            print(message)
            await asyncio.sleep(1)


asyncio.run(hello())