from django.urls import path
from .views import hello_world
from .views import stopDoShit
from .views import greet_user



urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('shit/', stopDoShit, name='shit_user'),
    path('greet/', greet_user, name='greet_user'),

]
