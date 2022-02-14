import asyncio
import websockets as ws
import json
from datetime import datetime, timedelta
from message_handler import message_handler
from currency_rate_memory import RateMemory
import logging


# async def handler(websocket, path):
#     while True:
#         message = await websocket.recv()
#         await consumer(message)

async def create_connection(cur_rates):
    url = 'wss://currency-assignment.ematiq.com'
    try:
        websocket = await ws.connect(url)
        print('Connected to ' + url)
    except Exception as error:

        logging.error('out')
        raise Exception(error)


    loop = asyncio.get_event_loop()
    task_send = loop.create_task(send_heartbeat(websocket))
    taks_receive = loop.create_task(listen(websocket, cur_rates))


    f, unf = await asyncio.wait([task_send, taks_receive], return_when=asyncio.FIRST_EXCEPTION)
    # loop.close()
    logging.warning('shit')
    logging.error(unf)

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
            await loop.run_in_executor(None, cur_rates.clean_mem())

            # receives message from server
            message = json.loads(await websocket.recv())

            if message['type'] == 'heartbeat':
                last_time = datetime.now()

            if datetime.now() > (last_time + timedelta(seconds=2.0)):
                asyncio.Task.cancel()
                raise Exception('TimeoutError')

            # processing of input message into output message
            back_message = await loop.run_in_executor(None, message_handler, message, cur_rates)
            #
            # print('==============================================')
            # print(f"server message: {message}")
            # print('----------------------------------------------')
            # print(f"my response: {back_message}")

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
        run()


if __name__ == "__main__":
    # simple run :)
    run()



