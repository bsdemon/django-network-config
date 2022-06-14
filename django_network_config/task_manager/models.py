from django import forms
from django.db import models
import uuid


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    hostname = models.CharField(max_length=200, unique=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    port = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.hostname}'


class TaskStatus(models.IntegerChoices):
    QUEUED = 1, 'Queued'
    PROCESSING = 2, 'Processing'
    SUCCESS = 3, 'Success'
    FAILURE = 4, 'Failure'
    TIMEOUT = 5, 'Timeout'


TASK_CHOICES = [
    (1, 'Queued'),
    (2, 'Processing'),
    (3, 'Success'),
    (4, 'Failure'),
    (5, 'Timeout'),
]


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.IntegerField(
        choices=TASK_CHOICES, default=TaskStatus.QUEUED)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    configuration = models.TextField()
    meta = models.TextField(blank=True, null=True)


class TaskReq(forms.ModelForm):
    id = models.UUIDField(default=uuid.uuid4)
    hostname = models.CharField(max_length=200)
    port = models.PositiveIntegerField()
    configuration = models.TextField()
    ip = models.GenericIPAddressField()
