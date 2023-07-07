from django.shortcuts import render
from backend.models import Faculty,FacultyCodeStatus
from backend.serializers import StudentSerializer
from SRAM.middleware import auth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

@api_view(['POST'])
def facultyCode(request):
   request = auth(request)
   data = request.data
   if data["facultyCode"]=='':
      return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
   codeStatus = ToggleCodeStatus(data["facultyCode"],data["classRoom"])
    
   
def ToggleCodeStatus(facultyCode,classRoom=""): #Helper Function to Toggle code status
   codeStatus = FacultyCodeStatus.objects.get(faculty=Faculty.objects.get(code=data['facultyCode']))
   codeStatus.status = not codeStatus.status
   codeStatus.classRoom = classRoom
   codeStatus.save()
   return codeStatus   