from rest_framework import serializers
from .models import Student,Faculty,Course,Batch, Attendance, QRCodeTable, BatchCourseFaculty

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
        
class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model= QRCodeTable
        fields = ['classRoom', 'qrCode']
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name','code']
        
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name', 'email', 'code','isActive']                

class BatchCourseFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchCourseFaculty
        fields = '__all__'
