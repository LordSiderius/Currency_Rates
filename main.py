import asyncio
import websockets as ws
import json
from currency_rate_memory import RateMemory
from message_handler import message_handler, error_handler
import threading
from subprocess import call
import logging
from datetime import datetime, timedelta
import time


def server():
    """
    Function to call dummy server.

    :return:
        None
    """
    call(["e:/Python_project/Currency_rates/venv/Scripts/python.exe", "test_space/server.py"])


async def handler():

    # initialization of currency rates memory
    cur_rates = RateMemory()

    # url = 'ws://localhost:8765'
    url = 'wss://currency-assignment.ematiq.com'

    websocket = await ws.connect(url)
    print('Connected to ' + url)

    loop = asyncio.get_event_loop()
    task_send = loop.create_task(producer_handler(websocket))
    task_receive = loop.create_task(consumer_handler(websocket, cur_rates))

    finished, pending = await asyncio.wait([task_send, task_receive], return_when=asyncio.FIRST_EXCEPTION)

    # task don't return anything, so only exception can break the loop
    for task in finished:
        print(task.exception())
        # raise Exception(task.exception())

    # close task, which are not finished
    for task in pending:
        task.cancel()


async def producer_handler(websocket):

    print('Sending heartbeats started...')

    while True:

        message = json.dumps({'type': 'heartbeat'})
        await websocket.send(message)
        print('==============================================')
        print('heartbeat send')

        await asyncio.sleep(1)

# async def miniservice(websocket):
#
#     result = []
#     while True:
#         message = await websocket.recv()
#         # print(message)
#
#         if not(message is None):
#             result.append(message)
#
#         if message is None:
#             return result

async def consumer_handler(websocket, cur_rates):

    print('Receiving from server started...')

    # stores time, when communication begun
    # last_time = datetime.now()

    async for message in websocket:
        try:
            response = message_handler(message, cur_rates)
            if response is not None:
                print(f"Response: {response}")
                await websocket.send(response)

        except Exception as error_msg:

            logging.error(error_msg)
            break

def run():



    try:
    # runs the application
        asyncio.run(handler())

    except Exception as error:
    #
        logging.error(error)
        print('Restarting application!')
        time.sleep(2)
        run()


if __name__ == '__main__':

    # DEBUG session
    DEBUG = False
    if DEBUG:
        processThread = threading.Thread(target=server)
        processThread.start()
        url = 'ws://localhost:8765'
        run()

    # simple run :)
    else:
        run()
