from django.shortcuts import render
from backend.models import Faculty,FacultyCodeStatus, OTPModel
from backend.serializers import StudentSerializer
from backend.views import generate_otp
from SRAM.middleware import auth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from SRAM.celery import app
from datetime import datetime, timedelta
import jwt
from SRAM.settings import env
from SRAM.constants import AUTHORIZATION_LEVELS
import bcrypt
import pytz



@api_view(['POST'])
def facultyCode(request):
   request = auth(request)
   data = request.data
   if data["facultyCode"]=='':
      return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
   codeStatus = ToggleCodeStatus(data["facultyCode"],data["classRoom"])
   
@api_view(['POST'])
def forgotPassword(request):
   data = request.data
   if data["otp"] == '' or data["email"] == '' or data['password'] == '':
      return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
   faculty = Faculty.objects.get(email=data["email"])
   if not faculty:
      return Response({'message': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
   otpModel = OTPModel.objects.get(email=data["email"])
   if not otpModel:
      return Response({'message': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
   
   if otpModel.expiry.replace(tzinfo=pytz.utc) < datetime.now().replace(tzinfo=pytz.utc):
      generate_otp(request)
      return Response({'message': 'OTP Expired, New OTP Has Been Sent To Email'}, status=status.HTTP_401_UNAUTHORIZED)

   if otpModel.otp == data["otp"]:
      faculty.salt = bcrypt.gensalt()
      faculty.setPassword(data['password'])
      faculty.save()
      otpModel.delete()
      return Response({'message': 'Password Changed'}, status=status.HTTP_200_OK)
   else:
      return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['POST'])
def login(request):
   data = request.data
   if data["email"] == '' or data['password'] == '':
      return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
   faculty = Faculty.objects.get(email=data["email"])
   if not faculty.checkPassword(data["password"]):
      return Response({'message': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
   # generate jwt
   payload = {
      'email': faculty.email,
      'name': faculty.name,
      'exp': datetime.utcnow() + timedelta(days=1),
      'iat': datetime.utcnow(),
      'authorizationLevel':AUTHORIZATION_LEVELS['FACULTY']
   }
   token = jwt.encode(payload, env("JWT_SECRET_KEY"), algorithm='HS256')
   return Response({'message':'Logged in Successfully', 'token': token}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getFaculty(request):
   request = auth(request, True)
   faculty = Faculty.objects.get(email=request.tokenData['email'])
   courses = []
   for course in faculty.courses:
      courses.append({
         'name': course.name,
         'code': course.code,
      })
   return Response({
      'name': faculty.name,
      'email': faculty.email,
      'courses': courses,
      'code': faculty.code,
      'created': faculty.created,
      'isActive':faculty.isActive,
   }, status=status.HTTP_200_OK)

   

@app.task
def AutoFalseCodeStatus(facultyCode, classRoom=""):
   codeStatus = FacultyCodeStatus.objects.get(faculty=Faculty.objects.get(code=facultyCode))
   codeStatus.status = False
   codeStatus.classRoom = classRoom
   codeStatus.save()
   return codeStatus  

def ToggleCodeStatus(facultyCode,classRoom=""): #Helper Function to Toggle code status
   codeStatus = FacultyCodeStatus.objects.get(faculty=Faculty.objects.get(code=facultyCode))
   codeStatus.status = not codeStatus.status
   codeStatus.classRoom = classRoom
   if codeStatus.status:
      AutoFalseCodeStatus.apply_async(args=[facultyCode,classRoom],eta=datetime.now()+timedelta(minutes=10))
   codeStatus.save()
   return codeStatus 
 
@api_view(['POST'])
def facultyBatchCourse():
   request = auth(request,'FACULTY')
   data = request.data
   faculty = Faculty.objects.get(email=request.tokenData['email'])
   if data['batch'] != '':
      faculty.batch = data['batch']
   if data['course'] != '':
      faculty.course = data['course']
   faculty.save()
   return Response({'message':'Batch and Course Updated'}, status=status.HTTP_200_OK)