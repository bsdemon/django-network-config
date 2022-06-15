import json
import redis

from django.core.management.base import BaseCommand
from django.conf import settings

import task_manager.utils as utils


class Command(BaseCommand):
    help = 'Dispatch config'

    def send_config(self, message):
        if message and isinstance(message.get('data', ''), (bytes, bytearray)):
            data = message.get('data', '').decode('utf8')
            json_data = json.loads(data)
            task_id = json_data['task_id']
            # ip = json_data['ip']
            ip = json_data['hostname']
            port = json_data['port']
            conf = json_data['configuration']
            utils.add_task_to_queue(ip, port, conf, task_id)

    def handle(self, *args, **kwargs):
        r = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT, db=settings.REDIS_DB)
        p = r.pubsub()
        p.psubscribe(settings.REDIS_CHANNEL)
        for message in p.listen():
            self.send_config(message)

