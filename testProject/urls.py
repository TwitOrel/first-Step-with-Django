"""
URL configuration for testProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from api.views import home, dashboard_view


urlpatterns = [
    # adding paths of API
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('', home, name='home'),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("dashboard/", include("api.urls")),
    path("login/", include("users.urls")),
]
