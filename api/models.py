from django.db import models
from django.utils.timezone import now


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100) 
    age = models.IntegerField() 

    def __str__(self):
        return f"{self.name} ({self.age})"

class Todo(models.Model):
    task = models.CharField(max_length=255)  
    completed = models.BooleanField(default=False)
    date = models.DateField(default=now)
    time = models.TimeField(default=now)


    def __str__(self):
        return f" {self.task} - Date: {self.date}, Time: {self.time}."