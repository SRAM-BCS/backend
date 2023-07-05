from django.shortcuts import render
from .models import Student, Course, Batch, BatchCourseFaculty, Faculty, Attendance, Codes, FacultyCodeStatus, OTPModel
from .serializers import StudentSerializer, AttendanceSerializer
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
from SRAM.constants import AUTHORIZATION_LEVELS
from SRAM.middleware import auth
from random import randint
from SRAM.utils import send_email

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
    request = auth(request, 'FACULTY')
    # fetch all student data
    students = Student.objects.all()
    # serialize data
    serializer = StudentSerializer(students, many=True)
    # return response   
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def student_with_email(request):
    # fetch student data
    request = auth(request, 'STUDENT')
    try:
        student = Student.objects.get(email=request.tokenData['email'])
        # serialize data
        serializer = StudentSerializer(student)
        # return response
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'message': 'Student Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def mark_attendance(request):
    request = auth(request, 'STUDENT')
    #  coursecode, teachercode,  batch code from request.tokenData
    data = request.data
    # check if data is valid
    if data['coursecode'] == '' or data['teachercode'] == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if course exists
    if not Course.objects.filter(code=data['coursecode']).exists():
        return Response({'message': 'Course Not Found'}, status=status.HTTP_404_NOT_FOUND)
    # check if faculty exists
    if not Faculty.objects.filter(code=data['teachercode']).exists():
        return Response({'message': 'Faculty Not Found'}, status=status.HTTP_404_NOT_FOUND)
    # check if faculty code is active
    facultyCodeStatus = FacultyCodeStatus.objects.get(faculty=Faculty.objects.get(code=data['teachercode']))
    if not facultyCodeStatus.status:
        return Response({'message': 'Faculty Code is not active'}, status=status.HTTP_401_UNAUTHORIZED)
    # make unique code 
    uniqueCode = data['coursecode']+';'+data['teachercode']+';'+request.tokenData['batch'].code
    # check if unique code exists
    if not Codes.objects.filter(uniqueCode=uniqueCode).exists():
        return Response({'message': 'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)
    # get BatchCourseFaculty Object
    batchCourseFaculty = BatchCourseFaculty.objects.get(batch=request.tokenData['batch'], course=Course.objects.get(code=data['coursecode']), faculty=Faculty.objects.get(code=data['teachercode']))
    # check if batchCourseFaculty exists
    if not batchCourseFaculty:
        return Response({'message': 'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)
    # check if attendance is already marked
    if Attendance.objects.filter(batchCourseFaculty=batchCourseFaculty, roll=Student.objects.get(email=request.tokenData['email']).roll, date=datetime.today()).exists():
        return Response({'message': 'Attendance already marked'}, status=status.HTTP_401_UNAUTHORIZED)
    # create new attendance object
    attendance = Attendance(batchCourseFaculty=batchCourseFaculty, roll=Student.objects.get(email=request.tokenData['email']).roll, date=datetime.today())
    # save attendance object
    attendance.save()
    # return response
    return Response({'message': 'Attendance Marked'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_student_attendance(request):
    request = auth(request, 'STUDENT')
    # get student by email
    student = Student.objects.get(email=request.tokenData['email'])
    # check if exists
    if not student:
        return Response({'message': 'Student Not Found'}, status=status.HTTP_404_NOT_FOUND)
    # get all attendance of student
    attendance = Attendance.objects.filter(roll=student.roll).get()
    # get BATCHFACULTYCOURSE object
    batchCourseFaculty = BatchCourseFaculty.objects.get(id=attendance.BCF_id)
    # check if exists
    if not batchCourseFaculty:
        return Response({'message': 'Attendance Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    # data
    data = {
        "roll": attendance.roll,
        "batch": batchCourseFaculty.batch.title,
        "course": batchCourseFaculty.course.name,
        "faculty": batchCourseFaculty.faculty.name,
        "date":attendance.date,
        "name": student.name,
        "email":student.email
    }
    # return response
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def generate_otp(request):
    otp = randint(100000, 999999)
    print(otp)
    email = request.POST.get("email")
    if not email:
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if email already in OTPModel
    if OTPModel.objects.filter(email=email).exists():
        otpModel = OTPModel.objects.get(email=email)
        otpModel.otp = otp
        otpModel.save()
    else:
        otpModel = OTPModel(email=email, otp=otp)
        otpModel.save()
    # send otp to email
    send_email(to_email=email, body="Your OTP is "+str(otp), subject="Attendance Management System")
    return Response({'message': 'OTP Sent'}, status=status.HTTP_200_OK)


