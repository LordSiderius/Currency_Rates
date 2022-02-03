# This is a currency rates script for Ematiq interview

import asyncio
import websockets as ws
import json
import time

def read_json(path):

    with open(path, 'r') as f:
        # perform file operations
        content = json.load(f)

    return str(content).replace("'","\"")

def stop():
    task.cancel()
    print('shit')


async def heart_beat(path):

    data = read_json(path)

    print('Starting Application')

    # t0 = time.time()
    # while True:
    #     a = time.time()
    #     print(a-t0)
    #     t0 = a

    async with ws.connect("wss://currency-assignment.ematiq.com") as connection:

        try:
            await asyncio.wait_for(connection.send(data), timeout=2)
            print("> {}".format(data))
            response = await asyncio.wait_for(connection.recv(), timeout=2)
            print("< {}".format(response))
        except asyncio.TimeoutError:
            print('timeout!')
            raise ValueError
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



#



start_app()





