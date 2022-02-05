# This is a currency rates script for Ematiq interview

import asyncio
import websockets as ws
import json
import time
from datetime import datetime
from currency_rate_memory import RateMemory

def read_json(path):

    with open(path, 'r') as f:
        # perform file operations
        content = json.load(f)

    return str(content).replace("'","\"")
#
# def stop():
#     task.cancel()
#     print('shit')

# def calculate(message):


async def response(connection):
    response = await asyncio.wait_for(connection.recv(), timeout=2)
    print("res: {}".format(response))
    with open('output.txt', 'a') as f:
        f.write(response + '\n')

async def request(connection, data):
    await connection.send(data)
    print("req: {}".format(data))
    task_respond = asyncio.create_task(asyncio.wait_for(response(connection), timeout=2))


async def heart_beat(path):

    data = read_json(path)

    print('Starting Application')

    # t0 = time.time()
    # while True:
    #     a = time.time()
    #     print(a-t0)
    #     t0 = a

    async with ws.connect("wss://currency-assignment.ematiq.com") as connection:


        # task_respond = asyncio.create_task(asyncio.wait_for(response(connection), timeout=2))

        while True:
            await asyncio.sleep(1)
            task_request = asyncio.create_task(request(connection, data))
            task_request
            print(datetime.now().second)




        # await task_request
        # try:
        #     await task_respond
        #     print("> {}".format(data))
        #     response = await asyncio.wait_for(connection.recv(), timeout=2)
        #     print("< {}".format(response))
        # except asyncio.TimeoutError:
        #     print('timeout!')
        #     raise ValueError
            # a = asyncio.get_running_loop()
            # print(a)
            # a.cancel()

def start_app():

    loop = asyncio.get_event_loop()
    # loop.create_task(heart_beat('heartbeat.json'))
    task = loop.create_task(heart_beat('heartbeat.json'))

    try:
        loop.run_forever()

    except:
        print('restarting application...')
        start_app()

# start_app()
rate_mem = RateMemory()

asyncio.run(heart_beat('heartbeat.json'))



