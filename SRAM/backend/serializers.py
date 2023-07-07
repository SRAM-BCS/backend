from rest_framework import serializers
from .models import Student,Faculty,Course,Batch, Attendance, QRCodeTable

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email', 'roll', 'profileImage', 'idImage','batch', 'created', 'updated', 'isActive', 'requestStatus']  
        
class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['title', 'code']        

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model= Attendance
        fields = ['BCF_id', 'roll', 'date']
        
class QRCode(serializers.ModelSerializer):
    class Meta:
        model= QRCodeTable
        fields = ['classRoom', 'qrCode']
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'code']
        
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name', 'email', 'code','password','created', 'updated', 'isActive']                
