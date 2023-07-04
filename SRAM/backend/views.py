from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from backend.schema import LoginRequest
import bcrypt
from datetime import datetime, timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api
import jwt
from SRAM.settings import env
from SRAM.constants import AUTHORIZATION_LEVEL

# Create your views here.
@api_view(['POST'])
def register(request):
    # get data from request
    data = request.data
    # check if data is valid
    if data['name'] == '' or data['email'] == '' or data['roll'] == '' or data['password'] == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if roll number already exists
    if Student.objects.filter(roll=data['roll']).exists():
        return Response({'message': 'Roll Number already exists'}, status=status.HTTP_400_BAD_REQUEST)
    # create new student object
    student = Student(name=data['name'], email=data['email'], roll=data['roll'], password=data['password'], salt = bcrypt.gensalt(), batch=data['batch'])
    # set password
    student.setPassword(data['password'])
    # get profileImage
    profileImage = request.FILES.get('profileImage', None)
    # upload profileImage to cloudinary
    if profileImage is not None:
        uploadResult = cloudinary.uploader.upload(profileImage)
        print(uploadResult['url'])
        student.profileImage = uploadResult['url']

    # get idImage
    idImage = request.FILES.get('idImage', None)
    # upload idImage to cloudinary
    if idImage is not None:
        uploadResult = cloudinary.uploader.upload(idImage)
        print(uploadResult['url'])
        student.idImage = uploadResult['url']
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
        return Response({'message': 'Not Found. Please Contact Your Admin.'}, status=status.HTTP_404_NOT_FOUND)
    # get student object
    student = Student.objects.get(email=data.email)
    # check if password is correct
    if not student.checkPassword(data.password):
        return Response({'message': 'Incorrect Password'}, status=status.HTTP_401_UNAUTHORIZED)
    # check if student is active
    if not student.isActive:
        return Response({'message': 'Account is not active'}, status=status.HTTP_401_UNAUTHORIZED)
    # use serializer
    serializer = StudentSerializer(student)
    # create jwt token
    refresh = jwt.encode({
        'name': serializer.data.name,
        'email': serializer.data.email,
        'roll': serializer.data.roll,
        'batch': serializer.data.batch,
        'authorizationLevel': AUTHORIZATION_LEVEL['STUDENT'],
        'isActive': serializer.data.isActive,
        'exp': datetime.utcnow() + timedelta(days=1)
    }, env("JWT_SECRET_KEY"), algorithm="HS256")
    # return response
    return Response({'message': 'Login Successful', 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)


@api_view(['GET'])
def student(request):
    # fetch all student data
    students = Student.objects.all()
    # serialize data
    serializer = StudentSerializer(students, many=True)
    # return response   
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def student_with_email(request):
    # fetch student data
    try:
        student = Student.objects.get(email=email)

    except Student.DoesNotExist:

@api_view(['POST'])
def mark_attendance(request):
#  coursecode, teachercode,  batch code from request.tokenData
