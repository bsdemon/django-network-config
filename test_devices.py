import asyncio
import aiohttp

ports = list(range(8000,8050))
url = 'http://localhost:{}'
results = []
task_dict = {}

def when_finished(fut):
    print("foo returned", fut.result())

def get_tasks(session):
    return [session.get(url.format(port), ssl=False) for port in ports]

async def make_single_task(session, port):
    await session.get(url.format(port))
    print(f'Task on port {port} is done')

async def check_device():
    async with aiohttp.ClientSession() as session:
        # for port in ports:
        #     task_dict[port] = await asyncio.create_task(session.get(url.format(port), ssl=False))      
        # ------------------------------
        # tasks = get_tasks(session)
        # responses = await asyncio.gather(*tasks)
        # ------------------------------
        tasks = [make_single_task(session, port) for port in ports]
        responses = await asyncio.gather(*tasks)
        print(responses)

# asyncio.run(check_device(ports))

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(coros))
# loop.close()

loop = asyncio.get_event_loop()
loop.set_debug(True)  # Enable debug
loop.run_until_complete(check_device())

print("Completed All Tasks")
