from django.shortcuts import render
from backend.models import Student, Admin, QRCodeTable, Batch, Course, Faculty, Attendance
from backend.serializers import StudentSerializer, AttendanceSerializer, BatchSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from backend.schema import LoginRequest
import bcrypt
from datetime import datetime, timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api
import qrcode
import base64
from io import BytesIO
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
    request = auth(request, 'ADMIN')
    data = request.data
    
    if data['roll'] == '' or data['statusNum'] == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    
    student = Student.objects.get(roll=data['roll'])
    student.requestStatus = Student.OptionEnum[f"OPTION{data['statusNum']}"]
    student.save()
    
    return Response({'message': 'Student Status set to'+Student.OptionEnum[f"OPTION{data['statusNum']}"]}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def save_new_admin(request):
    request = auth(request, 'ADMIN')
    data = request.data
    if data["email"]=='' or data["password"]=='':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        
    #Save a new admin object
    newAdmin = Admin(email=data["email"],password=data['password'])
    newAdmin.save()
    return Response({'message': 'New Admin Saved'}, status=status.HTTP_201_CREATED)
    

@api_view(['POST','GET'])
def QR(request):
    if(request.method=='POST'):
        request = auth(request, 'ADMIN')
        data = request.data
        if(data["classRoom"]==''):
            return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data['classRoom'])
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()    
        uploadResult = cloudinary.uploader.upload(
        "data:image/png;base64," + qr_base64,format="png")
        qrURL = uploadResult['secure_url']
        classQR = QRCodeTable.objects.get(classRoom=data['classRoom'])
        if(classQR is not None):
            classQR.qrCode = qrURL
        else:
            classQR = QRCodeTable(classRoom=data['classRoom'],qrCode=qrURL)
        classQR.save()         
        return Response({'message': 'New QR Generated', 'data':classQR}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        #Get classroom from request query
        classRoom = request.query_params.get('classRoom', None)
        if classRoom is None:
            return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        qr = QRCodeTable.objects.get(classRoom=classRoom)
        return Response({'message': 'QR Genrated','data':qr}, status=status.HTTP_200_OK)
    

# save_new_batch, get_all_batches, save_new_course, get_all_courses

@api_view(['POST','GET'])
def batch(request):
    if request.method == "POST":
        # request = auth(request, 'ADMIN')
        data = request.data
        if data["title"]=='' or data["code"]=='':
            return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        newBatch = Batch(title=data["title"],code=data["code"])
        newBatch.save()
        serializer = BatchSerializer(newBatch)
        return Response({'message': 'New Batch Saved', 'data':serializer.data}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        batches = Batch.objects.all()
        return Response({'message': 'All Batches','data':batches}, status=status.HTTP_200_OK)
        
    return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
def course(request): 
    if request.method == "POST":
        request = auth(request, 'ADMIN')
        data = request.data
        if data["name"]=='' or data["code"]=='':
            return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        newCourse = Course(name=data["name"],code=data["code"])
        newCourse.save()
        return Response({'message': 'New Course Saved'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        courses = Course.objects.all()
        return Response({'message': 'All Courses','data':courses}, status=status.HTTP_200_OK)    