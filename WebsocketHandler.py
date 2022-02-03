import asyncio
from contextlib import suppress
import websockets as ws
import json

class Periodic:
    def __init__(self, time):
        self.time = time
        self.is_started = False
        self._task = None

    def read_json(self, path):
        with open(path, 'r') as f:
            # perform file operations
            content = json.load(f)

        return str(content).replace("'", "\"")

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task


    async def _run(self):

        data = self.read_json('heartbeat.json')

        while True:
            await asyncio.sleep(self.time)
            async with ws.connect("wss://currency-assignment.ematiq.com") as connection:

                await connection.send(data)
                print("> {}".format(data))





async def main():
    p = Periodic(1)
    try:
        print('Start')
        await p.start()
        await asyncio.sleep(11.1)
        # print('Stop')
        # await p.stop()
    #
    finally:
        await p.stop()  # we should stop task finally

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())