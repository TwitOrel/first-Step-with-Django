from .views import register, login_user, logout_user, check_authentication, get_csrf_token, reset_password_request, reset_password_confirm
from django.urls import path

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('check-auth/', check_authentication, name='check_authentication'),
    path('get-csrf/', get_csrf_token, name='get_csrf_token'),
    path('forgot-password/', reset_password_request, name='reset_password_request'),
    path('reset-password/<uidb64>/<token>/', reset_password_confirm, name='reset_password_confirm'),

]
