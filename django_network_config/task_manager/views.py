from django.shortcuts import render

from .models import Task

def home(request):
    qs = Task.objects.all()
    context = {
        "task_list": qs
    }
    return render(request, "home.html", context=context)