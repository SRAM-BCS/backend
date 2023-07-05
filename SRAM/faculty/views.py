from django.shortcuts import render
from backend.models import Faculty,FacultyCodeStatus
from backend.serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

@api_view(['POST'])
def facultyCode(request):
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
