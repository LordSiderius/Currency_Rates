# Dummy server for debugging

import asyncio
import websockets
import random
import json


# async def send_message(websocket):
#     path = 'test_messages/mixed_messages.txt'
#     with open(path, 'r') as file:
#         text = file.readlines()
#         size = len(text)
#
#         while True:
#             # with probability of 30% will send message, otherwise it will return heartbeat
#             message = text[random.randint(0, size - 1)]
#
#             delay = random.random() * 2.0
#             await asyncio.sleep(delay)
#             await websocket.send(message)
#             print("Server: Message sent")



async def echo(websocket):

    try:
        async for message in websocket:
            # print('============================================================')
            # print('Message received by server:')
            # print(message)
            # print('============================================================')

            for i in range(random.randint(0, 2)):
                path = 'test_space/test_messages/mixed_messages.txt'
                with open(path, 'r') as file:
                    text = file.readlines()
                    size = len(text)
                    message = text[random.randint(0, size - 1)]
                    await websocket.send(message)
                    # print('Server sent message')


            message = json.loads(message)
            # print(message)
            path = 'test_space/test_messages/mixed_messages.txt'


            print('Server is alive')

            if message['type'] == 'heartbeat':
            #
            #     message = json.dumps(message)
            #     # simulation of server timeout, it can take server 3 secs to answer, which is greater
            #     # than 2 secs timeout of client
                delay = random.random() * 2.0
            #     # print('delay: ' + str(delay))
                await asyncio.sleep(delay)
            #     # send message
                await websocket.send(json.dumps(message))

            # with open(path, 'r') as file:
            #     text = file.readlines()
            #     size = len(text)
            #
            #     # convert message to string
            #     message = json.dumps(message)
            #
            #     # with probability of 30% will send message, otherwise it will return heartbeat
            #     if random.random() > 0.7:
            #         message = text[random.randint(0, size - 1)]
            #         # send message
            #         await websocket.send(message)


    except Exception as e:
        print('============================================================')
        print('Server Error:')
        print(e)
        print('============================================================')





async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == '__main__':

    while True:
        asyncio.run(main())
