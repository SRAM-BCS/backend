from django.shortcuts import render
from .models import Student, Course, Batch, BatchCourseFaculty, Faculty, Attendance, Codes, FacultyCodeStatus, OTPModel, VerifiedEmails, QRCodeTable
from .serializers import StudentSerializer, BatchSerializer, CourseSerializer, FacultySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from backend.schema import LoginRequest, RegisterRequest, ForgotPasswordRequest
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
from SRAM.utils import send_email, verify_user, convert_image_to_base64
import pytz

# Create your views here.
@api_view(['POST'])
def register(request):
    # get data from request
    data:RegisterRequest = request.data
    # check if data is valid
    if data['name'] == '' or data['email'] == '' or data['roll'] == '' or data['password'] == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if iiitm.ac.in domain
    if data['email'].split('@')[1] != 'iiitm.ac.in':
        return Response({'message': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
    
    # check if email in verified email
    if not VerifiedEmails.objects.filter(email=data['email']).exists():
        return Response({'message': 'Email not verified'}, status=status.HTTP_400_BAD_REQUEST)
    
    # check if roll number already exists
    if Student.objects.filter(roll=data['roll']).exists():
        return Response({'message': 'Roll Number already exists'}, status=status.HTTP_400_BAD_REQUEST)
    # create new student object
    student = Student(name=data['name'], email=data['email'], roll=data['roll'], password=data['password'], salt = bcrypt.gensalt(), batch=data['batch'])
    # set password
    student.setPassword(data['password'], bcrypt.gensalt())
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

    # delete verified email instance
    VerifiedEmails.objects.filter(email=data['email']).delete()

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
        'authorizationLevel': AUTHORIZATION_LEVELS['STUDENT'],
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
    # return Response(serializer.data, status=status.HTTP_200_OK)
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
    #  coursecode, teachercode, room code, batch code from request.tokenData
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
    
    # check if QR room code is present
    if not QRCodeTable.objects.filter(classRoom=data['classRoom']).exists():
        return Response({'message': 'QR Code Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    # make unique code 
    uniqueCode = data['coursecode']+';'+data['teachercode']+';'+request.tokenData['batch'].code+";"+data['classRoom']

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
    attendance = Attendance(batchCourseFaculty=batchCourseFaculty, roll=Student.objects.get(email=request.tokenData['email']).roll, date=datetime.today(), classRoom=data['classRoom'])
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


@api_view(['POST'])
def generate_otp(request):
    otp = randint(100000, 999999)
    print(otp)
    email = request.data["email"] 
    if not email:
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    
    # check if iiitm.ac.in domain
    if email.split('@')[1] != 'iiitm.ac.in':
        return Response({'message': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
   
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

@api_view(['POST'])
def verify_otp(request):
    otp = request.data["otp"]
    email = request.data["email"]
    if not otp or not email:
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if email already in OTPModel
    if OTPModel.objects.filter(email=email).exists():
        # delete the OTPModel instance
        otpModel = OTPModel.objects.get(email=email)
        # check if otp is correct
        if otpModel.otp != int(otp):
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
        if otpModel.expiry.replace(tzinfo=pytz.utc) < datetime.now().replace(tzinfo=pytz.utc):
            # generate new otp and send email then return
            generate_otp(request)
            return Response({'message': 'OTP Expired, New OTP Has Been Sent To Email'}, status=status.HTTP_401_UNAUTHORIZED)
        # create Verified Email Instance
        verifiedEmail = VerifiedEmails(email=email)
        verifiedEmail.save()
        # delete the OTPModel instance
        otpModel.delete()
        return Response({'message': 'Email Verified Successfully'}, status=status.HTTP_202_ACCEPTED)

@api_view(['PUT'])
def forgot_password(request):
    data: ForgotPasswordRequest = request.data
    if not data.newPassword or not data.otp or not data.email:
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check email domain
    if data.email.split('@')[1] != 'iiitm.ac.in':
        return Response({'message': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
    
    # check if email already in OTPModel
    if not OTPModel.objects.filter(email=data.email).exists():
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
    # delete the OTPModel instance
    otpModel = OTPModel.objects.get(email=data.email)
    # check if otp is correct
    if otpModel.otp != int(data.otp):
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
    # if otpModel.expiry.replace(tzinfo=pytz.utc) < datetime.now().replace(tzinfo=pytz.utc):
    #     # generate new otp and send email then return
    #     generate_otp(request)
    #     return Response({'message': 'OTP Expired, New OTP Has Been Sent To Email'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # delete the OTPModel instance
    # get student
    student = Student.objects.get(email=data.email)
    # check if student exists
    if not student:
        return Response({'message': 'Student Not Found'}, status=status.HTTP_404_NOT_FOUND)
    # set new password
    student.setPassword(data.newPassword, bcrypt.gensalt())
    # save student
    student.save()
    # delete otp from model
    otpModel.delete()
    # return response
    return Response({'message': 'Password Changed Successfully'}, status=status.HTTP_202_ACCEPTED)

# TODO: Once tested, remove the route and make it an internal function which will be used in the mark_attendance
@api_view(['POST'])
def face_verification(request):
    request = auth(request, 'STUDENT')
    # get student by email
    student = Student.objects.get(email=request.tokenData['email'])
    # check if exists
    if not student:
        return Response({'message': 'Student Not Found'}, status=status.HTTP_404_NOT_FOUND)
    # get image
    image = request.FILES['image']
    # get profile image from student
    profileImage = student.profileImage
    # check if profile image exists
    if not profileImage:
        return Response({'message': 'Profile Image Not Found'}, status=status.HTTP_404_NOT_FOUND)
    encoded_image = convert_image_to_base64(image.read())
    data = verify_user(img1=encoded_image, img2=profileImage)
    if data['verified']:
        return Response({'message': 'Verified', 'status':True}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Not Verified', 'status':False}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
def course(request):
    request = auth(request, 'STUDENT')
    # get student by email
    student = Student.objects.get(email=request.tokenData['email'])
    # check if exists
    if not student:
        return Response({'message': 'Student Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    batch = student.batch_id
    
    # get all the courses
    bcfObjs = BatchCourseFaculty.objects.filter(batch=Batch.objects.get(id=batch))
    course_faculty_array = []
    for fcb in bcfObjs:
        faculty = Faculty.objects.get(code=fcb.faculty.code)
        if not batch:
           return Response({'message':'Faculty Not Found'}, status=status.HTTP_404_NOT_FOUND)
        course = Course.objects.get(code=fcb.course.code)
        if not course:
           return Response({'message':'Course Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializedFaculty = FacultySerializer(batch).data
        serializedCourse = CourseSerializer(course).data
        course_faculty_array.append({'course':serializedCourse,'faculty':serializedFaculty})
    return Response({'message': 'Student Courses', 'data': course_faculty_array}, status=status.HTTP_200_OK)        


