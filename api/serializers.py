from rest_framework import serializers
from .models import User, Todo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'age'] 

class TodoSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d-%m-%Y'])
    time = serializers.TimeField(input_formats=['%H:%M:%S'])
    class Meta:
        model = Todo
        fields = ['id', 'task', 'completed', 'date', 'time']