from rest_framework import serializers
from .models import Student,Faculty,Course,Batch

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email', 'roll', 'profileImage', 'idImage','batch', 'created', 'updated', 'isActive', 'requestStatus']  
        
class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['name', 'course', 'faculty']        