from django.contrib import admin
from .models import Todo
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.


admin.site.register(Todo)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)