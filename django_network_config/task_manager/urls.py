from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.get_tasks, name='get_tasks'),
    path('set_tasks', csrf_exempt(views.set_tasks), name='ser_tasks'),

]