from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from sqlalchemy import create_engine, Text, select
from backend.schema import LoginRequest

# Create your views here.
@api_view(['POST'])
def register(request):
    # get data from request
    data:Student = request.data
    # check if data is valid
    if data['name'] == '' or data['email'] == '' or data['roll'] == '' or data['password'] == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if roll number already exists
    if Student.objects.filter(roll=data['roll']).exists():
        return Response({'message': 'Roll Number already exists'}, status=status.HTTP_400_BAD_REQUEST)
    # create new student object
    student = Student(name=data['name'], email=data['email'], roll=data['roll'])
    # save student object
    student.save()
    # return response
    return Response({'message': 'Student Registered'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    data:LoginRequest = request.data
    # check if data is valid
    if data.email == '' or data.password == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if student exists
    if not Student.objects.filter(email=data.email).exists():
        return Response({'message': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)
    # get student object
    student = Student.objects.get(email=data.email)
    # check if password is correct
    


@api_view(['GET'])
def student(request):
    # fetch all student data
    students = Student.objects.all()
    # serialize data
    serializer = StudentSerializer(students, many=True)
    # return response   
    return Response(serializer.data, status=status.HTTP_200_OK)



