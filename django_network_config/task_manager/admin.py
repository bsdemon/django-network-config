from django.contrib import admin
from .models import Device, Task
from django.utils.html import format_html

# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'hostname', 'ip', 'created')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'status_colored', 'timestamp')

    @admin.display(description='Status')
    def status_colored(self, obj):
        colors = {
            1: 'gray',
            2: 'yellow',
            3: 'green',
            4: 'red',
            5: 'black',
        }
        return format_html(
            '<b style="color:{};">{}</b>',
            colors[obj.status],
            obj.get_status_display(),
        )


admin.site.register(Device, DeviceAdmin)
admin.site.register(Task, TaskAdmin)
