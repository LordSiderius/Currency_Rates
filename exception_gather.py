import asyncio
import random

async def problem():
    while True:
        number = random.random()
        if number <= 0.9:
            print('ok')
        else:
            print('NOK')
            raise Exception('process failed')

        await asyncio.sleep(0.5)

async def problem2():
    while True:
        number = random.random()
        if number <= 0.8:
            print('ok2')
        else:
            print('NOK2')
            raise Exception('process2 failed')

        await asyncio.sleep(1)

async def run_process():

    loop = asyncio.get_event_loop()
    task1 = loop.create_task(problem())
    task2 = loop.create_task(problem2())

    result, pending = await asyncio.wait([task1, task2], return_when=asyncio.FIRST_EXCEPTION)

    result = dict(result)

    print(f"result: {result['exception']}")
    print(f"pending: {pending}")

    # result = await asyncio.gather(task1, task2, return_exceptions=True)
    # raise Exception(result)

if __name__ == '__main__':
    try:
        asyncio.run(run_process())
    except Exception as error_msg:
        print(error_msg)
