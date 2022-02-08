import asyncio
import websockets as ws
import json
from datetime import datetime
from currency_rate_memory import RateMemory
from message_handler import message_handler, error_handler
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

async def heartbeat(rates_mem):
    print('starting conenction...')

    async with ws.connect("wss://currency-assignment.ematiq.com") as connection:
        while True:
            data = json.dumps({'type': 'heartbeat'})
            await connection.send(data)
            print("req: {}".format(data))
            try:
                message = await asyncio.wait_for(connection.recv(), timeout=2)
                message = json.loads(message)
                print('original res: {}'.format(message))
                back_message = message_handler(message, rates_mem)
                if back_message is not None:
                    await connection.send(json.dumps(back_message))
                    print('back message ' + str(back_message))
            except asyncio.exceptions.TimeoutError:
                error_message = error_handler('TimeoutError')
                await connection.send(json.dumps(error_message))
                # print(error_message)
                # raise Exception('Timeout error')

            rates_mem.clean_mem()
            await asyncio.sleep(1)


def run(loop):
    cur_rates = RateMemory()

    try:
        loop.run_until_complete(heartbeat(cur_rates))

    except Exception as error:
        print(error)
        run(loop)

loop = asyncio.get_event_loop()
loop.set_exception_handler(None)
run(loop)
