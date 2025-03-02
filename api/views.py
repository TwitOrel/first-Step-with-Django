from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework import status
from .models import User, Todo
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html')


def home_view(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")

@api_view(['GET', 'POST'])
@csrf_exempt
@permission_classes([IsAuthenticated]) 
def todo_list(request):
    if request.method == 'GET': 
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    if request.method == 'POST': 
        request.data["user"] = request.user.id 
        serializer = TodoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_detail(request, pk):

    try:
        todo = Todo.objects.get(pk=pk, user=request.user) 
    except Todo.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo, context={'request': request})
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        todo.delete()
        return Response({'message': 'Todo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
