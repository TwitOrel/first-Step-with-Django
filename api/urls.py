from .views import hello_world, stopDoShit, greet_user
from .views import user_list, user_detail, todo_list, todo_detail
from django.contrib import admin
from django.urls import path




urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('shit/', stopDoShit, name='shit_user'),
    path('greet/', greet_user, name='greet_user'),


    # CRUD
    path('todos/', todo_list, name='todo_list'),
    path('todos/<int:pk>/', todo_detail, name='todo_detail'),
    path('users/', user_list, name='user_list'),  # יצירה וקריאה של כל המשתמשים
    path('users/<int:pk>/', user_detail, name='user_detail'),  # קריאה, עדכון ומחיקה לפי ID
]
