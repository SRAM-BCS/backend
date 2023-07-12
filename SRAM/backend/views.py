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
    data = request.data
    data = LoginRequest(data['email'], data['password'])
    # check if data is valid
    if data.email == '' or data.password == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if student exists
    if not Student.objects.filter(email=data.email).exists():
        return Response({'message': 'Not Found. Please Contact Your Admin.'}, status=status.HTTP_404_NOT_FOUND)
    try:
        # get student object
        student = Student.objects.get(email=data.email)
        # check if password is correct
        if not student.checkPassword(data.password):
            return Response({'message': 'Incorrect Password'}, status=status.HTTP_401_UNAUTHORIZED)
        # check if student is active
        if not student.isActive:
            return Response({'message': 'Account is not active'}, status=status.HTTP_401_UNAUTHORIZED)

        if student.requestStatus != 1:
            msg = 'Your Account is Pending for Approval' if (student.requestStatus) else 'Your Account is Rejected'
            return Response({'message': msg}, status=status.HTTP_401_UNAUTHORIZED)

    except:
        return Response({'message': 'Not Found. Please Contact Your Admin.'}, status=status.HTTP_400_BAD_REQUEST)
    # use serializer
    serializer = StudentSerializer(student)
    # create jwt token
    refresh = jwt.encode({
        'name': serializer.data["name"],
        'email': serializer.data["email"],
        'roll': serializer.data["roll"],
        'batch': serializer.data["batch"],
        'authorizationLevel': AUTHORIZATION_LEVELS['STUDENT'],
        'isActive': serializer.data["isActive"],
        'exp': datetime.utcnow() + timedelta(days=1)
    }, env("JWT_SECRET_KEY"), algorithm="HS256")
    # return response
    return Response({'message': 'Login Successful', 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)


@api_view(['GET'])
def student(request):
    authorized,request = auth(request,'STUDENT')
    if not authorized : 
        return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)

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
    authorized,request = auth(request,'STUDENT')
    if not authorized : 
        return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)

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
    authorized,request = auth(request,'STUDENT')
    if not authorized : 
      return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)
   
    #  coursecode, teachercode, room code, batch code from request.tokenData
    data = request.data
    # check if data is valid
    if data['coursecode'] == '' or data['teachercode'] == '' or data['classRoom'] == '':
        return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    # check if course exists
    if not Course.objects.filter(code=data['coursecode']).exists():
        return Response({'message': 'Course Not Found'}, status=status.HTTP_404_NOT_FOUND)
    # check if faculty exists
    if not Faculty.objects.filter(code=data['teachercode']).exists():
        return Response({'message': 'Faculty Not Found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        # check if faculty code is active
        facultyCodeStatus = FacultyCodeStatus.objects.get(faculty=Faculty.objects.get(code=data['teachercode']))
        if facultyCodeStatus.status == False:
            return Response({'message': 'Faculty Code is not active. You cannot mark your attendance'}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({'message': 'Faculty Code is not active'}, status=status.HTTP_401_UNAUTHORIZED)
    # check if QR room code is present
    if not QRCodeTable.objects.filter(classRoom=data['classRoom']).exists():
        return Response({'message': 'QR Code Not Found'}, status=status.HTTP_404_NOT_FOUND)
    if facultyCodeStatus.classRoom != data['classRoom']:
        return Response({'message': 'Invalid ClassRoom Entered'}, status=status.HTTP_400_BAD_REQUEST)
    # make unique code 
    # uniqueCode = data['coursecode']+';'+data['teachercode']+';'+request.tokenData['batch'].code+";"+data['classRoom']

    # # check if unique code exists
    # if not Codes.objects.filter(uniqueCode=uniqueCode).exists():
    #     return Response({'message': 'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        # get BatchCourseFaculty Object
        batchCourseFaculty = BatchCourseFaculty.objects.get(batch=request.tokenData['batch'], course=Course.objects.get(code=data['coursecode']), faculty=Faculty.objects.get(code=data['teachercode']))
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    # check if attendance is already marked
    if Attendance.objects.filter(BCF_id=batchCourseFaculty, roll=Student.objects.get(email=request.tokenData['email']), date=datetime.today()).exists():
        return Response({'message': 'Attendance already marked'}, status=status.HTTP_401_UNAUTHORIZED)
    # create new attendance object
    attendance = Attendance(BCF_id=batchCourseFaculty, roll=Student.objects.get(email=request.tokenData['email']), date=datetime.today(), classRoom=QRCodeTable.objects.get(classRoom=data['classRoom']))
    # save attendance object
    attendance.save()
    # return response
    return Response({'message': 'Attendance Marked'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_student_attendance(request):
    authorized,request = auth(request,'STUDENT')
    if not authorized : 
        return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # get student by email
        student = Student.objects.get(email=request.tokenData['email'])
        # get all attendance of student
        attendance = Attendance.objects.filter(roll=student.roll).get()
        # get BATCHFACULTYCOURSE object
        batchCourseFaculty = BatchCourseFaculty.objects.get(id=attendance.BCF_id)
    except:
        return Response({'message': 'Attendance Not Found'}, status=status.HTTP_400_BAD_REQUEST)
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
    try:
        # delete the OTPModel instance
        otpModel = OTPModel.objects.get(email=data.email)
    except:
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
    # check if otp is correct
    if otpModel.otp != int(data.otp):
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
    # if otpModel.expiry.replace(tzinfo=pytz.utc) < datetime.now().replace(tzinfo=pytz.utc):
    #     # generate new otp and send email then return
    #     generate_otp(request)
    #     return Response({'message': 'OTP Expired, New OTP Has Been Sent To Email'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # delete the OTPModel instance
    # get student
    try:
        student = Student.objects.get(email=data.email)
    except:
        return Response({'message': 'Student Not Found'}, status=status.HTTP_400_BAD_REQUEST)
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
    authorized,request = auth(request,'STUDENT')
    if not authorized : 
        return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # get student by email
        student = Student.objects.get(email=request.tokenData['email'])
    except:
        return Response({'message': 'Student Not Found'}, status=status.HTTP_400_BAD_REQUEST)
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
    authorized,request = auth(request,'STUDENT')
    if not authorized : 
        return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # get student by email
        student = Student.objects.get(email=request.tokenData['email'])
    except:
        return Response({'message': 'Student Not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
    batch = student.batch
    
    # get all the courses
    bcfObjs = BatchCourseFaculty.objects.filter(batch=batch)
    course_faculty_array = []
    for fcb in bcfObjs:
        try:
            faculty = Faculty.objects.get(code=fcb.faculty.code)
            course = Course.objects.get(code=fcb.course.code)
        except:
            return Response({'message':'Faculty or Course Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        serializedFaculty = FacultySerializer(faculty).data
        serializedCourse = CourseSerializer(course).data
        course_faculty_array.append({'course':serializedCourse,'faculty':serializedFaculty})
    return Response({'message': 'Student Courses', 'data': course_faculty_array}, status=status.HTTP_200_OK)        


