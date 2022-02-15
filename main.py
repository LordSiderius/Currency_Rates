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

    """
    call(["e:/Python_project/Currency_rates/venv/Scripts/python.exe", "test_space/server.py"])


async def handler(url):
    """
    Connection handler. initialize connection to websocket and run sending and receiving tasks
    """

    # initialization of currency rates memory
    cur_rates = RateMemory()

    # initialization of connection to given url
    websocket = await ws.connect(url)
    print('Connected to ' + url)

    # creates separate tasks for sending and receiving
    loop = asyncio.get_event_loop()
    task_send = loop.create_task(producer_handler(websocket))
    task_receive = loop.create_task(consumer_handler(websocket, cur_rates))

    # run the tasks
    finished, pending = await asyncio.wait([task_send, task_receive], return_when=asyncio.FIRST_EXCEPTION)

    # task don't return anything, so only exception can break the loop
    for task in finished:
        logging.warning(task.exception())
        raise Exception(task.exception())

    # close task, which are not finished
    for task in pending:
        task.cancel()


async def producer_handler(websocket):
    """
    The function producer_handler(websocket) is sending heartbeat to websocket every second
    """

    print('Sending heartbeats started...')

    # loop runs forever
    while True:
        try:
            message = json.dumps({'type': 'heartbeat'})
            # timeout of two second in case of connection error
            await asyncio.wait_for(websocket.send(message), timeout=2)
            # print('==============================================')
            # print('heartbeat send') # heartbeat for DEBUG

            await asyncio.sleep(1)

        except Exception as error:
            raise Exception(error)


async def consumer_handler(websocket, cur_rates):
    """
    The Function consumer_handler(websocket, cur_rates) receiving messages from server and sending corresponding answer.
    """

    print('Receiving from server started...')

    # stores time, when communication begun
    last_time = datetime.now()
    while True:

        # call function to try to clean memory
        cur_rates.clean_mem()

        try:
            # raise an exception, when heartbeat is send more than after 2 secs
            if datetime.now() > (last_time + timedelta(seconds=2)):
                logging.error('timeout')
                raise Exception('2 sec limit for receiving from server exceeded')

            # listening to server
            res = await asyncio.wait_for(websocket.recv(), timeout=2)
            # print(f"message: {res}") # message for DEBUG

            # handler which is bulding a message with converted currency or an error message
            answer = message_handler(res, cur_rates)
            # print(f"answer: {answer}")# answer for DEBUG

            # stores last time, when heartbeat was received from server
            if answer == 'heartbeat':
                last_time = datetime.now()
            else:
                await asyncio.wait_for(websocket.send(answer), timeout=2)

        # catches timeout
        except asyncio.TimeoutError:
            logging.warning(asyncio.TimeoutError)
            raise Exception(asyncio.TimeoutError)

        # catches any other issue
        except Exception as e:
            logging.warning(e)
            raise Exception(e)


def run(url):
    """
    The run(url) is called to start the communication process
    """
    try:
    # runs the application
        asyncio.run(handler(url))

    # caych errors, which are corrupting connection
    except Exception as error:
        # connection errors are not send to server but being print to console
        logging.error(error)

        # try to restart communication
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
