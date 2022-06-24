import asyncio
import json
import threading
from typing import Dict
import aiohttp
import uvloop
from task_manager.models import Task, TaskStatus
import threading
from asgiref.sync import sync_to_async

running_tasks = []
waiting_tasks = []


@sync_to_async
def set_task_status(event, task_id, ip, response=None):
    status = TaskStatus.TIMEOUT
    result = json.loads(response) if response else None
    if result:
        if result['Status'] == 'Ok':
            status = TaskStatus.SUCCESS
        elif result['Status'] == 'Error':
            status = TaskStatus.FAILURE
        running_tasks.remove(ip)
    Task.objects.filter(id=task_id).update(status=status, meta=result)
    if len(waiting_tasks) > 0:
        for t in waiting_tasks:
            if t['ip'] == ip:
                waiting_tasks.remove(t)
                event.queue.put_nowait(t)


async def aiohttp_post(url):
    conn = aiohttp.TCPConnector(
        verify_ssl=True,
        use_dns_cache=False,
        ssl_context=None,
        ssl=None,
        limit=200,
        enable_cleanup_closed=False,
    )
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.post(url, ssl=False) as response:
            result = await response.text()
            return result


async def send_task(item: Dict, event):
    res = await aiohttp_post(f"http://{item['ip']}:{item['port']}")
    try:
        await set_task_status(event, item['task_id'], item['ip'], res)
        print(f"{item['ip']} Response is - {res} {item['task_id']}")
    except Exception as e:
        print(f'Error sending task -  {e}')


def add_task(event: threading.Event):
    _sentinel = 'STOP_LOOP'

    async def main():
        uvloop.install()
        event.loop = asyncio.get_running_loop()
        event.queue = task_queue = asyncio.Queue()
        event.set()
        while True:
            item = await task_queue.get()

            if item == _sentinel:
                task_queue.task_done()
                break

            if type(item) is dict:
                running_tasks.append(item['ip'])
                task = asyncio.create_task(send_task(item, event), name=item)
                task.add_done_callback(lambda _: task_queue.task_done())
        await task_queue.join()

    asyncio.run(main())
