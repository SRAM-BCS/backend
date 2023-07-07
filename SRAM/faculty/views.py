from django.shortcuts import render
from backend.models import Faculty,FacultyCodeStatus
from backend.serializers import StudentSerializer
from SRAM.middleware import auth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from SRAM.celery import app
from datetime import datetime, timedelta




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
   if faculty.otp == data["otp"]:
      faculty.setPassword(data['password'])
      faculty.save()
      return Response({'message': 'Password Changed'}, status=status.HTTP_200_OK)
   else:
      return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

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

  
 