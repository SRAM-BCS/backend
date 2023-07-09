from django.shortcuts import render
from backend.models import Student, Admin, QRCodeTable, Batch, Course, Faculty, Attendance, OTPModel
from backend.views import generate_otp
from backend.serializers import StudentSerializer, AttendanceSerializer, BatchSerializer, FacultySerializer, QRCodeSerializer
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
import random
import string
from io import BytesIO
import jwt
from SRAM.settings import env
from SRAM.constants import AUTHORIZATION_LEVELS
from SRAM.middleware import auth
import pytz
from SRAM.utils import send_email

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
    try:
        student = Student.objects.get(roll=data['roll'])
        student.requestStatus = Student.OptionEnum[f"OPTION{data['statusNum']}"]
        student.save()
    except:
        return Response({'message': 'Unable to Find Studen'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message': 'Student Status set to'+Student.OptionEnum[f"OPTION{data['statusNum']}"]}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def save_new_admin(request):
    request = auth(request, 'ADMIN')
    data = request.data
    if data["email"]=='' or data["password"]=='':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        
    #Save a new admin object
    newAdmin = Admin(email=data["email"],password=data['password'])
    newAdmin.setPassword(data['password'])
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
        classQR = QRCodeTable(classRoom=data['classRoom'],qrCode=qrURL)
        classQR.save()        
        serializedData = QRCodeSerializer(classQR) 
        return Response({'message': 'New QR Generated', 'data':serializedData.data}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        #Get classroom from request query
        classRoom = request.query_params.get('classRoom', None)
        if classRoom is None:
            return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        qr = QRCodeTable.objects.get(classRoom=classRoom)
        serializedData = QRCodeSerializer(qr)
        return Response({'message': 'QR Genrated','data':qr}, status=status.HTTP_200_OK)
    

# save_new_batch, get_all_batches, save_new_course, get_all_courses

@api_view(['POST','GET'])
def batch(request):
    if request.method == "POST":
        request = auth(request, 'ADMIN')
        data = request.data
        if data["title"]=='' or data["code"]=='':
            return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        newBatch = Batch(title=data["title"],code=data["code"])
        newBatch.save()
        serializer = BatchSerializer(newBatch)
        return Response({'message': 'New Batch Saved', 'data':serializer.data}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        try:
            batches = Batch.objects.all()
            return Response({'message': 'All Batches','data':batches}, status=status.HTTP_200_OK)
        except:
            return Response({'message': "No Batches Found"}, status=status.HTTP_400_BAD_REQUEST)
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
        try:
            courses = Course.objects.all()
            return Response({'message': 'All Courses','data':courses}, status=status.HTTP_200_OK)
        except:
            return Response({'message': "No Courses Found"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
def forgot_password(request):
    data = request.data
    if data["email"]=='' or data["newPassword"]=='' or data["otp"]=='':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        admin = Admin.objects.get(email=data["email"])
    except:
        return Response({'message': 'No Admin Found With The Email'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # get email from otpmodel
        otpModel = OTPModel.objects.get(email=data["email"])
        # check if otp is valid
        if otpModel.otp != data["otp"]:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({'message': 'Please Use Correct Email'}, status=status.HTTP_400_BAD_REQUEST)
    # if otpModel.expiry.replace(tzinfo=pytz.utc) < datetime.now().replace(tzinfo=pytz.utc):
    #     # generate new otp and send email then return
    #     generate_otp(request)
    #     return Response({'message': 'OTP Expired, New OTP Has Been Sent To Email'}, status=status.HTTP_401_UNAUTHORIZED)
    admin.setPassword(data["newPassword"], bcrypt.gensalt())
    # change password
    admin.save()
    # # delete otpModel
    otpModel.delete()
    return Response({'message': 'Password Changed'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def admin_login(request):
    data = request.data
    if data["email"]=='' or data["password"]=='':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        admin = Admin.objects.get(email=data["email"])
        if not admin.checkPassword(data["password"]):
            return Response({'message': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
        # set jwt token
        token = jwt.encode({'email': admin.email, 'authorizationLevel': AUTHORIZATION_LEVELS['ADMIN']}, env("JWT_SECRET_KEY"), algorithm="HS256")
        # return token
        return Response({'message': 'Login Successful', 'token': token}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'No Admin Found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_admins(request):
    admins = Admin.objects.all()
    list_admins = []
    for admin in admins:
        list_admins.append(admin.email)

    return Response({'message': 'All Admins', 'data': list_admins}, status=status.HTTP_200_OK)

@api_view(['POST','GET'])
def faculty(request):
    if request.method == 'POST':
        # request = auth(request, 'ADMIN')
        data = request.data
        if data["name"]=='' or data["email"]=='':
            return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        newFaculty = Faculty(name=data["name"],email=data["email"].lower())
        newFaculty.code = generateCode(data["name"])
        newFaculty.salt = bcrypt.gensalt()
        password = generatePassword()
        newFaculty.setPassword(password)
        newFaculty.save()
        serializedData = FacultySerializer(newFaculty)
        return Response({'message': 'New Faculty Saved','data':serializedData.data, 'password':password}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        try:
            faculties = Faculty.objects.filter(isActive=True)
            serializedData = FacultySerializer(faculties, many=True)
            return Response({'message': 'All Faculties','data':serializedData.data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': "No Faculties Found"}, status=status.HTTP_400_BAD_REQUEST)
    
    
def generateCode(name):
    code = ''
    #code should be First character of each word in name
    for word in name.split(' '):
        code+=word[0]
    matchingCodes = Faculty.objects.filter(code__startswith=code, isActive = True)
    if len(matchingCodes) > 0:
        code+='-'+str(len(matchingCodes)+1)
    return code    

def generatePassword(length=10):
    special_char = random.choice(['@', '#', '$'])
    digits = random.sample(string.digits, 2)
    letters = random.sample(string.ascii_letters, 7)
    password = special_char + digits[0] + digits[1] + ''.join(letters)
    password = ''.join(random.sample(password, len(password)))  # Shuffle the characters randomly
    return password
