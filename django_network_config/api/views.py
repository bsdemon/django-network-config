from copy import copy

from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import TaskSerializer, DeviceSerializer
from task_manager.models import Device, Task
from task_manager.service import RedisService


@api_view(['GET'])
def get_task_status(request, uuid):
    try:
        task = Task.objects.get(pk=uuid)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_running_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_task(request):

    req_data = copy(request.data)
    device_serializer = DeviceSerializer(data=req_data, many=False)
    if not device_serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST, data=device_serializer.error_messages)

    dev, _ = Device.objects.filter(hostname=req_data['hostname']).get_or_create(
        **device_serializer.validated_data)

    req_data['device'] = dev.pk
    serializer = TaskSerializer(data=req_data)

    if serializer.is_valid(raise_exception=True):

        task = Task.objects.create(**serializer.validated_data)
        redis_service = RedisService()
        req_data['task_id'] = str(task.id)
        req_data['device'] = str(req_data['device'])
        redis_resp = redis_service.publish_data(
            settings.REDIS_CHANNEL, req_data)
        resp = {
            'task_id': task.id,
            'subscribers_count': redis_resp
        }

        return Response(resp)
