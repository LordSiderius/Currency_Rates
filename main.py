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


async def handler(url):

    # initialization of currency rates memory
    cur_rates = RateMemory()

    websocket = await ws.connect(url)
    print('Connected to ' + url)

    loop = asyncio.get_event_loop()
    task_send = loop.create_task(producer_handler(websocket))
    task_receive = loop.create_task(consumer_handler(websocket, cur_rates))

    finished, pending = await asyncio.wait([task_send, task_receive], return_when=asyncio.FIRST_EXCEPTION)

    # task don't return anything, so only exception can break the loop
    for task in finished:
        logging.warning(task.exception())
        raise Exception(task.exception())

    # close task, which are not finished
    for task in pending:
        task.cancel()


async def producer_handler(websocket):

    print('Sending heartbeats started...')

    while True:
        try:
            message = json.dumps({'type': 'heartbeat'})
            await asyncio.wait_for(websocket.send(message), timeout=2)
            print('==============================================')
            print('heartbeat send')

            await asyncio.sleep(1)
        except Exception as error:
            raise Exception(error)


async def consumer_handler(websocket, cur_rates):
    # cur_rates.records_lifespan = 1/120 # DEBUG
    print('Receiving from server started...')

    # stores time, when communication begun
    last_time = datetime.now()
    while True:
        # try to clean memory
        cur_rates.clean_mem()
        try:
            # print((last_time + timedelta(seconds=2)) - datetime.now() )
            if datetime.now() > (last_time + timedelta(seconds=2)):
                logging.error('timeout')
                raise Exception('2 sec limit exceeded')

            res = await asyncio.wait_for(websocket.recv(), timeout=2)
            print(f"message: {res}")
            answer = message_handler(res, cur_rates)
            print(f"answer: {answer}")

            if answer == 'heartbeat':
                logging.warning('heartbeat')
                last_time = datetime.now()
            else:
                await asyncio.wait_for(websocket.send(answer), timeout=2)

        except asyncio.TimeoutError:
            logging.warning(asyncio.TimeoutError)
            raise Exception(asyncio.TimeoutError)

        except Exception as e:
            logging.warning(e)
            raise Exception(e)


def run(url):

    try:
    # runs the application
        asyncio.run(handler(url))

    except Exception as error:
        logging.error(error)
        print('Restarting application!')
        time.sleep(2)
        run(url)


if __name__ == '__main__':

    # DEBUG session
    DEBUG = False
    if DEBUG:
        processThread = threading.Thread(target=server)
        processThread.start()
        url = 'ws://localhost:8765'
        run(url)

    # simple run :)
    else:
        url = 'wss://currency-assignment.ematiq.com'
        run(url)
