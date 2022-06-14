import json
import multiprocessing
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError
from requests.exceptions import ConnectionError

from django.conf import settings

from task_manager.models import Task, TaskStatus

manager = multiprocessing.Manager()
running_tasks = manager.list()
waiting_tasks = manager.list()


def add_next_task_to_queue():
    if(len(waiting_tasks) > 0):
        for t in waiting_tasks:
            if t['ip'] not in running_tasks:
                waiting_tasks.remove(t)
                add_task_to_queue(t['ip'], t['port'], t['conf'], t['task_id'])


def set_task_status(task_id, ip, response=None):
    status = TaskStatus.TIMEOUT
    result = json.loads(response.text) if response else None
    if result:
        if result['Status'] == 'Ok':
            status = TaskStatus.SUCCESS
        elif result['Status'] == 'Error':
            status = TaskStatus.FAILURE
        running_tasks.remove(ip)
    Task.objects.filter(id=task_id).update(status=status, meta=result)

    add_next_task_to_queue()


def get_request(ip, port):
    url = f'http://{ip}:{port}'
    response = requests.get(url, timeout=settings.TIMEOUT)
    return f'Task on {url} is done with {response.text}'


def post_request(ip, port, conf, task_id):
    url = f'http://{ip}:{port}'
    response = ''
    try:
        response = requests.post(url, timeout=settings.TIMEOUT)
        print(f'Task on {url} is done with {response.text} - {task_id}')
    except (ConnectionError, MaxRetryError, NewConnectionError):
        set_task_status(task_id, ip, response)
    except Exception as e:
        print(f'Task on {url} -- TIME OUT -- {task_id}')
        print(e)

    set_task_status(task_id, ip, response)


def add_task_to_queue(ip, port, conf, task_id):
    if ip not in running_tasks:
        running_tasks.append(ip)
        process_task(ip, port, conf, task_id)
    else:
        a_dict = dict(
            ip=ip,
            port=port,
            conf=conf,
            task_id=task_id
        )
        waiting_tasks.append(a_dict)


def process_task(ip, port, conf, task_id):
    p = multiprocessing.Process(target=post_request, args=[
                                ip, port, conf, task_id])
    p.start()
