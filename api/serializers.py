from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d-%m-%Y'])
    time = serializers.TimeField(input_formats=['%H:%M:%S'])
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Todo
        fields = ['id', 'task', 'completed', 'date', 'time', 'user']