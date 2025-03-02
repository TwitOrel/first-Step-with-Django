from .views import todo_list, todo_detail
from django.contrib import admin
from django.urls import path




urlpatterns = [
    # CRUD
    path('todos/', todo_list, name='todo_list'),
    path('todos/<int:pk>/', todo_detail, name='todo_detail'),
]
