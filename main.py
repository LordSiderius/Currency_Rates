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


async def create_connection(cur_rates):

    url = 'ws://localhost:8765'
    # url = 'wss://currency-assignment.ematiq.com'

    try:
        websocket = await ws.connect(url)
        print('Connected to ' + url)

    except Exception as error:
        logging.error('out')
        raise Exception(error)

    loop = asyncio.get_event_loop()
    task_send = loop.create_task(send_heartbeat(websocket))
    task_receive = loop.create_task(listen(websocket, cur_rates))

    try:
        # results = await asyncio.gather(task_send, task_receive, return_exceptions=True)
        done, pending = await asyncio.wait([task_send, task_receive], return_when=asyncio.FIRST_EXCEPTION)
        # loop.close()
        logging.warning('shit')
        logging.error(done)

    except:
        raise Exception('shiting')


async def send_heartbeat(websocket):

    print('Sending heartbeats started...')

    while True:

        try:
            await websocket.send(json.dumps({'type': 'heartbeat'}))
            print('==============================================')
            print('heartbeat send')

        except Exception as error:
            raise Exception(error)

        await asyncio.sleep(1)


async def listen(websocket, cur_rates):

    print('Receiving from server started...')

    # stores time, when communication begun
    last_time = datetime.now()

    while True:

        try:
            loop = asyncio.get_running_loop()
            # call function to clean memory
            # await loop.run_in_executor(None, cur_rates.clean_mem)

            # receives message from server
            message = await websocket.recv()
            message = json.loads(message)
            print(f"server message: {message}")

            if message['type'] == 'heartbeat':
                last_time = datetime.now()

            if datetime.now() > (last_time + timedelta(seconds=2.0)):
                logging.warning('time exceeded')
                # asyncio.Task.cancel()
                raise Exception('TimeoutError')

            # processing of input message into output message
            back_message = loop.run_in_executor(None, message_handler, message, cur_rates)
            #
            print('==============================================')
            print(f"server message: {message}")
            print('----------------------------------------------')
            print(f"my response: {back_message}")

            # sending back message if there is a one
            if back_message is not None:
                await loop.create_task(websocket.send(json.dumps(back_message)))

        except Exception as error:
            raise Exception(error)


def run():

    # initialization of currency rates memory
    cur_rates = RateMemory()

    try:
        # runs the application
        asyncio.run(create_connection(cur_rates))

    except Exception as error:

        logging.error(error)
        print('Restarting application!')
        time.sleep(2)
        run()


# if __name__ == "__main__":
#
#     run()


if __name__ == '__main__':

    # DEBUG session
    DEBUG = True
    if DEBUG:
        processThread = threading.Thread(target=server)
        processThread.start()
        url = 'ws://localhost:8765'
        run()

    # simple run :)
    else:
        run()
