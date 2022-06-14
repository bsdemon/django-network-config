from rest_framework import serializers

from task_manager.models import Device, Task, TaskReq


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        extra_kwargs = {
            'hostname': {'validators': []},
        }


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        if validated_data:
            dev_instance = Device.objects.filter(
                hostname=validated_data['hostname']).get_or_create(**validated_data)
            task = Task(
                device=dev_instance,
                configuration=validated_data['configuration']
            )
        return Task.objects.create(task)

    def update(self, validated_data):
        if validated_data:
            dev_instance = Device.objects.filter(
                hostname=validated_data['hostname']).get_or_create(**validated_data)
            task = Task(
                device=dev_instance,
                configuration=validated_data['configuration']
            )
        return Task.objects.create(task)


class TaskReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskReq
        fields = '__all__'
