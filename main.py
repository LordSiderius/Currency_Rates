import asyncio
import websockets as ws
import json
from currency_rate_memory import RateMemory
from message_handler import message_handler, error_handler
import threading
from subprocess import call


def server():
    """
    Function to call dummy server.

    :return:
        None
    """
    call(["e:/Python_project/Currency_rates/venv/Scripts/python.exe", "test_space/server.py"])


async def heartbeat(rates_mem, url):
    print('starting connection...')

    # starts the connection with server
    async with ws.connect(url) as connection:
        # Connection is executed forever
        while True:
            # message for server is coverted to str
            data = json.dumps({'type': 'heartbeat'})

            try:
                # sending data to server
                await connection.send(data)

                # waiting to receive message from server with timeout 2 secs
                in_message = await asyncio.wait_for(connection.recv(), timeout=2.0)

                # message is loaded as json
                message = json.loads(in_message)

                # message with new currency rate is created
                back_message = message_handler(message, rates_mem)

                # if there is a return, message is sent back to server
                if back_message is not None:
                    await connection.send(json.dumps(back_message))

            # Exception for timeout
            except asyncio.exceptions.TimeoutError:

                raise Exception('TimeoutError - server is not responding')

            # The rest of the exceptions coming from the functions
            except Exception as error_msg:

                error_message = error_handler(error_msg)
                await connection.send(json.dumps(error_message))

            finally:
                # call function to check if currency rates memory can be cleared, execute if needed
                rates_mem.clean_mem()

            # print('Communication is running!')
            await asyncio.sleep(1)


def run(url="wss://currency-assignment.ematiq.com"):
    # get event loop
    loop = asyncio.get_event_loop()

    # creates object to store currency rates into memory
    cur_rates = RateMemory()

    try:
        loop.run_until_complete(heartbeat(cur_rates, url=url))

    # when exception connected to connection issue occurs it is printed into console and application is reset
    except Exception as error:
        print(error)
        run(url=url)


if __name__ == '__main__':

    # DEBUG session
    DEBUG = False
    if DEBUG:
        processThread = threading.Thread(target=server)
        processThread.start()
        url = 'ws://localhost:8765'
        run(url=url)

    # common session
    else:
        run()
