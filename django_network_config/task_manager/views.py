from django.shortcuts import render
from django.http import request, HttpResponse, HttpResponseNotAllowed

# Create your views here.
def get_tasks(request):
    return HttpResponse("You're at the task_manager index.")

def set_tasks(request):
    if  request.method == "POST":
        print(request.body)
        return HttpResponse('Ok')
    return HttpResponseNotAllowed('Method not allowed')