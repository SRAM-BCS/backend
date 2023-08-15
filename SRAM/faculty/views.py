from django.shortcuts import render
from django.db.models import Count, F,ExpressionWrapper, FloatField
from backend.models import Faculty,FacultyCodeStatus, OTPModel, BatchCourseFaculty, Course,  Batch, Attendance, QRCodeTable
from backend.serializers import StudentSerializer, BatchCourseFacultySerializer, BatchSerializer, CourseSerializer
from backend.views import generate_otp
from SRAM.middleware import auth
from SRAM.utils import convert_json_to_pdf_and_upload
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
   authorized,request = auth(request,'FACULTY')
   if not authorized : 
      return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)
   data = request.data
   if data["facultyCode"]=='':
      return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
   if data["classRoom"]:
      try:
         classRoom = QRCodeTable.objects.get(classRoom=data["classRoom"])
      except Exception as e:
         return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   codeStatus = ToggleCodeStatus(data["facultyCode"],data["classRoom"])
   return Response({'message': "codeStatus changed"}, status=status.HTTP_200_OK)
   
@api_view(['PUT'])
def forgotPassword(request):
   data = request.data
   if data["otp"] == '' or data["email"] == '' or data['password'] == '':
      return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
   try:   
      faculty = Faculty.objects.get(email=data["email"])
   except Exception as e:  
      print(str(e)) 
      return Response({'message': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
   
   try:
      otpModel = OTPModel.objects.get(email=data["email"])
   except Exception as e:
      print(str(e))
      return Response({'message': 'Invalid Email. OTP not found'}, status=status.HTTP_400_BAD_REQUEST)
   
   if otpModel.expiry.replace(tzinfo=pytz.utc) < datetime.now().replace(tzinfo=pytz.utc):
      generate_otp(request)
      return Response({'message': 'OTP Expired, New OTP Has Been Sent To Email'}, status=status.HTTP_401_UNAUTHORIZED)

   if otpModel.otp == data["otp"]:
      faculty.setPassword(data['password'], bcrypt.gensalt())
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
   try :   
      faculty = Faculty.objects.get(email=data["email"].lower())
   except Exception as e: 
      print(str(e)) 
      return Response({'message': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
   if not faculty.checkPassword(data["password"]): 
      return Response({'message': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
   # generate jwt
   payload = {
      'email': faculty.email,
      'name': faculty.name,
      'authorizationLevel':AUTHORIZATION_LEVELS['FACULTY'],
      'isActive':faculty.isActive,
   }
   token = jwt.encode(payload, env("JWT_SECRET_KEY"), algorithm='HS256')
   return Response({'message':'Logged in Successfully', 'token': token}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getFaculty(request):
   authorized,request = auth(request,'FACULTY')
   if not authorized : 
      return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)
   data = request.data
   try:
    faculty = Faculty.objects.get(email=request.tokenData['email'])
   except Exception as e: 
         print(str(e))
         return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
   courses = []
   bcfObjs = BatchCourseFaculty.objects.filter(faculty=faculty)
   for bcf in bcfObjs:
      courses.append({
         'name': bcf.course.name,
         'code': bcf.course.code,
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
   try:   
      codeStatus = FacultyCodeStatus.objects.get(faculty=Faculty.objects.get(code=facultyCode))
   except Exception as e: 
         print(str(e))
         return Response({'message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
   codeStatus.status = False
   if classRoom != "":
      codeStatus.classRoom = classRoom
   codeStatus.save()
   return codeStatus  

def ToggleCodeStatus(facultyCode,classRoom=""): #Helper Function to Toggle code status
   try:   
      codeStatus = FacultyCodeStatus.objects.get(faculty=Faculty.objects.get(code=facultyCode))
   except Exception as e: 
      codeStatus = FacultyCodeStatus(faculty=Faculty.objects.get(code=facultyCode))
   codeStatus.status = not codeStatus.status
   if(classRoom != ""):      
      codeStatus.classRoom = classRoom
   # if codeStatus.status:
   #    AutoFalseCodeStatus.apply_async(args=[facultyCode,classRoom],eta=datetime.now()+timedelta(minutes=10))
   codeStatus.save()
   return codeStatus 
 
@api_view(['POST','GET'])
def facultyBatchCourse(request):
   authorized,request = auth(request,'FACULTY')
   if not authorized : 
      return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)
   if request.method == 'POST':
      data = request.data
   #data={"email","batchCode","courseCode"}
      try:
         faculty = Faculty.objects.get(email=data['email'].lower())
         batch = Batch.objects.get(code=data['batchCode'])
         course = Course.objects.get(code=data['courseCode'])
      except Exception as e: 
         print(str(e))
         return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
      bcfObj= BatchCourseFaculty(batch=batch,course=course,faculty=faculty)
      bcfObj.save()
   # serialize = BatchCourseFacultySerializer(bcfObj)
      return Response({'message':'Batch, Course and Faculty Added'}, status=status.HTTP_201_CREATED)
   elif request.method == 'GET':
      data = request.query_params
      print(data['email'].lower())
      fcbObj = BatchCourseFaculty.objects.filter(faculty=Faculty.objects.get(email=data['email'].lower()))
      batch_course_array = []
      for fcb in fcbObj:
         try:
            faculty = Faculty.objects.get(email=data['email'].lower())
         except Exception as e: 
            print(str(e))
            return Response({'message': 'Invalid Data for Faculty'}, status=status.HTTP_400_BAD_REQUEST)   
         try:
            batch = Batch.objects.get(code=fcb.batch.code)
         except Exception as e: 
            print(str(e))
            return Response({'message': 'Invalid Data for Batch'}, status=status.HTTP_400_BAD_REQUEST)
         course = Course.objects.get(code=fcb.course.code)
         if not course:
            return Response({'message':'Course Not Found'}, status=status.HTTP_404_NOT_FOUND)
         serializedBatch = BatchSerializer(batch).data
         serializedCourse = CourseSerializer(course).data
         batch_course_array.append({'course':serializedCourse,'batch':serializedBatch})
             
      return Response({'message':' Courses and Batches for the Faculty ', 'data':batch_course_array}, status=status.HTTP_200_OK)

@api_view(['POST'])
def facultyBatchCourseAttendance(request):
   authorized,request = auth(request,'FACULTY')
   if not authorized : 
      return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)
   
   if request.method == 'POST':
      data = request.data
      print(data)
      try:   
         # faculty = Faculty.objects.get(email=data['email'].lower())
         batch = Batch.objects.get(code=data['batchCode'])
         course = Course.objects.get(code=data['courseCode'])
      except Exception as e: 
         print(str(e))
         return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
      attendanceStats = attendanceStatistics(course,batch)
      attendanceDayWise = get_attendance_report_by_date(course,batch)
      # uploaded_url = convert_json_to_pdf_and_upload(attendanceStats)
      return Response({'message':'Attendance Details',"data":{"attendanceStats":attendanceStats,"attendanceDayWise":attendanceDayWise}}, status=status.HTTP_200_OK)
   else:
      return Response({'message':'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)   
   
   #Attendance report for  Batch x Course date wise
def get_attendance_report_by_date(course, batch): #course and batch objects
   attendance_report = Attendance.objects.filter(
        BCF_id__course=course,
        BCF_id__batch=batch
    ).order_by('date', 'roll__roll')
   attendance_by_date = {}
# Loop through the attendance records
   for attendance in attendance_report:
      date = attendance.date
      date_str = date.strftime("%d-%b-%Y") 
      attObj =attendance.roll.roll
    # Check if the date is already a key in the dictionary
      if date_str in attendance_by_date:
        # Append the attendance record to the existing array
         attendance_by_date[date_str].append(attObj)
      else:
        # Create a new array with the attendance record
        attendance_by_date[date_str] = [attObj]

   return attendance_by_date  

def attendanceStatistics(course,batch): #In terms of percentage
    tot = Attendance.objects.filter(BCF_id__batch=batch,BCF_id__course=course).values('date').distinct().count()
    attendance_report = Attendance.objects.filter(
        BCF_id__course=course,
        BCF_id__batch=batch
    ).values('roll__roll').annotate(
        total_attendance = Count('id'),
        ).order_by('roll__roll')
    for record in attendance_report:
      total_attendance = record['total_attendance']
      record['total_classes'] = total_classes
      attendance_percentage = round((total_attendance * 100.0) / tot if tot != 0 else 0,2)
      record['attendance_percentage'] = attendance_percentage
    return attendance_report
 
 
@api_view(['POST'])
def getAttendanceStatsPDF(request):
   authorized,request = auth(request,'FACULTY')
   if not authorized : 
      return Response({'message': 'Authorization Error! You are not Authorized to Access this Information'}, status=status.HTTP_401_UNAUTHORIZED)
      
 