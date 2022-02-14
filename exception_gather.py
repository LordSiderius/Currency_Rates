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

async def run_process():

    loop = asyncio.get_event_loop()

    result = await asyncio.gather(loop.create_task(problem()), return_exceptions=True)
    raise Exception(result[0])

if __name__ == '__main__':
    try:
        asyncio.run(run_process())
    except Exception as error_msg:
        print(error_msg)
