from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models


class Todo(models.Model):
    task = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    date = models.DateField(default=now)
    time = models.TimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"User: {self.user if self.user != None else 'No User'}, Task: {self.task}"