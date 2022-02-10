import asyncio
import websockets as ws
import json
from currency_rate_memory import RateMemory
from message_handler import message_handler, error_handler


async def heartbeat(rates_mem):

    print('starting connection...')
    url = 'ws://localhost:8765' # DEBUG
    # url = "wss://currency-assignment.ematiq.com"


    async with ws.connect(url) as connection:
        while True:
            print('-----------------------------------------------------------------------------------------')
            data = json.dumps({'type': 'heartbeat'})
            await asyncio.wait_for(connection.send(data), timeout=0.2)
            print("out message: {}".format(data))

            try:
                message = await asyncio.wait_for(connection.recv(), timeout=2)
                message = json.loads(message)
                print('in message : {}'.format(message))

                # DEBUG recording
                # if message['type'] == "message":

                    # with open('output.txt', 'a') as f:
                    #     f.write(json.dumps(message) + '\n')
                # DEBUG recording end

                back_message = message_handler(message, rates_mem)

                if back_message is not None:
                    await connection.send(json.dumps(back_message))
                    print('back message ' + str(back_message))

            except asyncio.exceptions.TimeoutError:
                # print('original res: {}'.format(message))
                error_message = error_handler('TimeoutError - Sever is not responding')

                await connection.send(json.dumps(error_message))
                print('Error message: ' + str(error_message))
                raise Exception('TimeoutError - Sever is not responding')

            except Exception as error_msg:
                # print('original res: {}'.format(message))
                error_message = error_handler(error_msg)

                await connection.send(json.dumps(error_message))
                print('Error message: ' + str(error_message))


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
