from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view



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