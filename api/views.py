from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, TodoSerializer
from django.shortcuts import render
from rest_framework import status
from .models import User, Todo

# for todoList
def home(request):
    return render(request, 'index.html')

@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':  # הצגת כל המשימות
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    if request.method == 'POST':  # הוספת משימה חדשה
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        todo.delete()
        return Response({'message': 'Todo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def hello_world(request):
    print(f"Received request: {request.method} {request.path}")
    return Response({"message": "Hello, Django API! - here is Orel"})


@api_view(['GET'])
def stopDoShit(request):
    print(f"Received request: {request.method} {request.path} dont make shit again!")
    return Response({"message": "Hello, Django API! - dont do shit again you ear me!!"})

@api_view(['POST'])  # לוודא שהפונקציה מוגדרת לקבל POST
def greet_user(request):
    # קבלת הנתונים מהבקשה
    name = request.data.get('name', 'אורח')
    age = request.data.get('age', 'לא ידוע')

    # בניית תגובה מותאמת אישית
    message = f"היי {name}, אתה בן {age} שנים!"
    print(message)
    return Response({"greeting": message})


### for the CRUD 

# קריאה של כל המשתמשים ויצירת משתמש חדש
@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':  # קריאה של כל המשתמשים
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':  # יצירת משתמש חדש
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# קריאה, עדכון או מחיקה של משתמש לפי ID
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  # קריאת משתמש לפי ID
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':  # עדכון משתמש לפי ID
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':  # מחיקת משתמש לפי ID
        user.delete()
        return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
