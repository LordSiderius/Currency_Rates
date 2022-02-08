import asyncio
import websockets as ws
import json
from datetime import datetime
from currency_rate_memory import RateMemory
from message_handler import message_handler


async def request(connection, rates_mem):
    data = '{"type":"heartbeat"}'
    await asyncio.wait_for(connection.send(data), timeout=0.5)
    print("req: {}".format(data))
    # print(datetime.now().second)

    asyncio.create_task(response(connection, rates_mem))
    await asyncio.sleep(1)


async def response(connection, rates_mem):
    message = await asyncio.wait_for(connection.recv(), timeout=2)
    message = json.loads(message)

    print('original res: {}'.format(message))
    back_message = message_handler(message, rates_mem)
    print('new res: {}'.format(back_message))

    if back_message is not None:
        # connection.send(str(message))

        print('send')


async def send_message(connection, message):
    try:
        connection.send(message)
    except:
        pass

async def heartbeat(rates_mem):

    async with ws.connect("wss://currency-assignment.ematiq.com") as connection:

        while True:

            try:
                await request(connection, rates_mem)
            except asyncio.exceptions.TimeoutError:

                print('Shit happened!')
                break


# loop = asyncio.get_event_loop()
# loop.create_task(heartbeat())
# loop.run_forever()

def start():
    rates_mem = RateMemory()
    # rates_mem.records_lifespan = 1/1800
    asyncio.run(heartbeat(rates_mem))
    start()


rate_memory = RateMemory()
start()
