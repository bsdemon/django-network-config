from django.urls import path

from . import views

urlpatterns = [
    path('get_task_status/<uuid:uuid>/', views.get_task_status, name='get_task_status'),
    path('get_all_running_tasks', views.get_all_running_tasks, name='get_all_running_tasks'),
    path('create_task', views.create_task, name='create_task'),

]