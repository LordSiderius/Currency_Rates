# Dummy server for debugging

import asyncio
import websockets
import random
import json


async def echo(websocket):
    try:
        async for message in websocket:
            print('============================================================')
            print('Message received by server:')
            print(message)
            print('============================================================')

            message = json.loads(message)
            # path = 'test_messages/invalid_date_currency.txt'
            path = 'test_space/test_messages/mixed_messages.txt'
            # path = 'test_messages/mixed_messages.txt'


            with open(path, 'r') as file:
                text = file.readlines()
                size = len(text)

                if message['type'] == 'heartbeat':

                    # convert message to string
                    message = json.dumps(message)

                    # with probability of 30% will send message, otherwise it will return heartbeat
                    if random.random() > 0.3:
                        message = text[random.randint(0, size - 1)]


                    # simulation of server timeout, it can take server 3 secs to answer, which is greater
                    # than 2 secs timeout of client
                    delay = random.random() * 5.0
                    print('delay: ' + str(delay))
                    await asyncio.sleep(delay)

                    # send message
                    await websocket.send(message)

    except Exception as e:
        print('============================================================')
        print('Server Error:')
        print(e)
        print('============================================================')





async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
