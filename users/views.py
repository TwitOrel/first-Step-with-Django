from django.utils.decorators import decorator_from_middleware
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny



def login_view(request):
    return render(request, "login.html")

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid reset link'}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Invalid or expired reset link'}, status=400)

    # שינוי הסיסמה
    new_password = request.data.get('password')
    if not new_password:
        return Response({'error': 'Password is required'}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password successfully reset'})

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_request(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=400)

    # יצירת לינק לאיפוס סיסמה
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    # בניית הלינק החדש - שולח לדף login עם פרמטרים ב-URL
    reset_link = request.build_absolute_uri(
        reverse('login') + f'?reset=1&uidb64={uid}&token={token}'
    )

    # print(f"\n🔗 Password Reset Link: {reset_link}\n") # can print the link to terminal if mail doesnt working
    subject = 'Reset Your Password - Todo List'
    message = f"""
    Hi {user.username},

    We received a request to reset your password for your Todo List account.

    Click the link below to reset your password:
    {reset_link}

    If you didn't request this, please ignore this email.

    Thanks,
    The Todo List Team
    """

    send_mail(
        subject,
        message,
        'oreltwito3@gmail.com', 
        [email],
        fail_silently=False,
    )

    return Response({'message': 'Password reset link generated (check email)'})


## register
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Missing required fields'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=400)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'User registered successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


## login
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    identifier = request.data.get('identifier')
    password = request.data.get('password')

    user = User.objects.filter(email=identifier).first() or User.objects.filter(username=identifier).first()

    if user and user.check_password(password): 
        login(request, user)  
        request.session.save() 

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'Login successful',
            'token': token.key
        })

    return Response({'error': 'Invalid credentials'}, status=400)


## check conecting
@api_view(['GET'])
def check_authentication(request):
    if request.user.is_authenticated:
        return Response({'authenticated': True, 'username': request.user.username})
    return Response({'authenticated': False})

## logout

@csrf_exempt
@api_view(['POST'])
def logout_user(request):
    logout(request)
    request.session.flush()
    return Response({'message': 'Logged out successfully'})

@ensure_csrf_cookie 
def get_csrf_token(request):
    return JsonResponse({'message': 'CSRF cookie set'})