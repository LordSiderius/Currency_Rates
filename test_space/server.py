# Dummy server for debugging

import asyncio
import websockets
import random
import json
import logging

async def echo(websocket):

    try:
        async for message in websocket:
            print('Server is alive')
            # print('============================================================')
            # print('Message received by server:')
            # print(message)
            # print('============================================================')

            g = json.loads(message)

            if g['type'] == 'heartbeat':

                for i in range(random.randint(0, 2)):
                    path = 'test_space/test_messages/mixed_messages.txt'
                    # path = 'test_space/test_messages/valid_messages.txt'
                    with open(path, 'r') as file:
                        text = file.readlines()
                        size = len(text)
                        message = text[random.randint(0, size - 1)]
                        await websocket.send(message)
            #
            #     message = json.dumps(message)
            #     # simulation of server timeout, it can take server 3 secs to answer, which is greater
            #     # than 2 secs timeout of client
            #     delay = random.random() * 3.0
                delay = 1.0
            #     # print('delay: ' + str(delay))
                await asyncio.sleep(delay)
            #     # send message
                await websocket.send(json.dumps(g))

    except Exception as e:
        print('============================================================')
        logging.error(f"Server Error: {e}")
        print('============================================================')

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == '__main__':

    while True:
        asyncio.run(main())
