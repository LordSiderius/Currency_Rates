import asyncio
import websockets as ws
import json
from datetime import datetime
from currency_rate_memory import RateMemory
from message_handler import message_handler
import time

async def request(connection):
    data = '{"type":"heartbeat"}'
    await connection.send(data)
    print(datetime.now().second)
    print("req: {}".format(data))





async def response(connection):
    message = await connection.recv()
    message = json.loads(message)
    print('original res: {}'.format(message))
    await asyncio.sleep(1)
    return str(message)

async def heartbeat(loop):
    # print('tack')
    async with ws.connect("wss://currency-assignment.ematiq.com") as connection:
        while True:
            # loop = asyncio.get_event_loop()
            # tasks = []
            #
            # tasks.append(await request(connection))
            # tasks.append(await response(connection))
            # f, unf = loop.run_until_complete(await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION))
            a, unf = loop.run_forever(await asyncio.wait([await request(connection), await response(connection)], return_when=asyncio.FIRST_EXCEPTION))

            for task in a:
                print('finished: %s' % str(task.result()))

            for task in unf:
                print('unfinished: %i' % len(unf))
                print(task)

            await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(heartbeat(loop))
    # print('tick')
    # loop.close()

