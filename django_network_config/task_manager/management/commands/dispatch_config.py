import json
import threading
import redis

from django.core.management.base import BaseCommand
from django.conf import settings

# import task_manager.utils as utils
from task_manager.utils import add_task, running_tasks, waiting_tasks


class Command(BaseCommand):
    help = 'Dispatch config'

    def send_config(self, message, tasks, loop):
        if message and isinstance(message.get('data', ''), (bytes, bytearray)):
            data = message.get('data', '').decode('utf8')
            json_data = json.loads(data)
            task_id = json_data['task_id']
            # ip = json_data['ip']
            ip = json_data['hostname']
            port = json_data['port']
            conf = json_data['configuration']
            
            task_data = dict(
                ip=ip,
                port=port,
                conf=conf,
                task_id=task_id
            )

            if ip in running_tasks:
                waiting_tasks.append(task_data)
                return

            loop.call_soon_threadsafe(tasks.put_nowait, (task_data))

    def handle(self, *args, **kwargs):
        event = threading.Event()
        th = threading.Thread(target=add_task, args=(event,))
        th.start()
        event.wait()
        tasks, loop = event.queue, event.loop

        r = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT, db=settings.REDIS_DB)
        p = r.pubsub()
        p.psubscribe(settings.REDIS_CHANNEL)
        for message in p.listen():
            self.send_config(message, tasks, loop)

