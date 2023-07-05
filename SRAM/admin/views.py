from django.shortcuts import render
from backend.models import Student, Course, Batch, BatchCourseFaculty, Faculty, Attendance, Codes, FacultyCodeStatus
from backend.serializers import StudentSerializer, AttendanceSerializer
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
# Create your views here.

@api_view(['GET'])
def pending_student_status(request):
    request = auth(request, 'ADMIN')

    limit = request.query_params.get('limit', None)
    offset = request.query_params.get('skip', None)
        
    pending_students = Student.objects.filter(requestStatus=Student.OptionEnum.OPTION2).order_by('-id')
        
    if limit is not None:
            pending_students = pending_students[:int(limit)]
        
    if offset is not None:
            pending_students = pending_students[int(offset):]
        
    serializer = StudentSerializer(pending_students, many=True)
    serialized_students = serializer.data
        
    return Response(serialized_students)

@api_view(['POST'])
def save_student_status(request):
    request = auth(request, 'STUDENT')
    data = request.data
    
    if data['roll'] == '' or data['statusNum'] == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    
    student = Student.objects.get(roll=data['roll'])
    student.requestStatus = Student.OptionEnum[f"OPTION{data['statusNum']}"]
    student.save()
    
    return Response({'message': 'Student Status set to'+Student.OptionEnum[f"OPTION{data['statusNum']}"]}, status=status.HTTP_201_CREATED)