from django.db import models
from cloudinary.models import CloudinaryField
import bcrypt
# Create your models here.
class Student(models.Model):
    class OptionEnum(models.TextChoices):
        OPTION1 = '1', 'Accepted'
        OPTION2 = '2', 'Pending'
        OPTION3 = '0', 'Denied'
    name = models.CharField("Name", max_length=240)
    email = models.EmailField()
    password = models.CharField("Password", max_length=240)
    roll = models.CharField("RollNumber", max_length=240, primary_key=True)
    profileImage = CloudinaryField('image',null=True) # for recognition
    idImage = CloudinaryField('image',null=True) # for verification
    requestStatus = models.CharField(max_length=1, choices=OptionEnum.choices, default=OptionEnum.OPTION2)
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, default=None)
    created = models.DateField(auto_now_add=True)
    updated= models.DateField(auto_now_add=True)
    isActive = models.BooleanField(default=False)
    salt = models.CharField("Salt")
    def __str__(self):
        return self.name
    def setPassword(self, password):
        self.password = bcrypt.hashpw(password.encode('utf8'), self.salt)
    def checkPassword(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))
    
class Faculty(models.Model):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField()
    password = models.CharField("Password", max_length=240)
    created = models.DateField(auto_now_add=True)
    code = models.CharField("Code", max_length=240, primary_key=True)
    courses = models.ManyToManyField('Course', through='BatchCourseFaculty')
    isActive = models.BooleanField(default=False)
    salt = models.CharField("Salt")
    def __str__(self):
        return self.name    
    def setPassword(self, password):
        self.password = bcrypt.hashpw(password.encode('utf8'), self.salt)
    def checkPassword(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

class Batch(models.Model):
    title = models.CharField("Title", max_length=240)
    code = models.CharField("Code", max_length=240, primary_key=True)
    courses = models.ManyToManyField('Course', through='BatchCourseFaculty')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    
class Course(models.Model):
    name = models.CharField("Name", max_length=240)
    code = models.CharField("Code", max_length=240, primary_key=True)
    batches = models.ManyToManyField(Batch, through='BatchCourseFaculty')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Codes(models.Model):
    uniqueCode = models.CharField("UniqueCode", max_length=240, primary_key=True)
    isActive = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name    

class BatchCourseFaculty(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    

class Attendance(models.Model):
    BCF_id = models.ForeignKey(BatchCourseFaculty, on_delete=models.CASCADE)
    roll = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class QRCode(models.Model):
    classRoom = models.CharField("ClassRoom", max_length=240)
    qrCode = models.CharField("QRCode", max_length=240, primary_key=True) #url of the QR
    def __str__(self):
        return self.name
    

class FacultyCodeStatus(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    lastActivated = models.DateField("LastActivated")
    def __str__(self):
        return self.name
    
    
class Admin(models.Model):
    email = models.EmailField()
    password = models.CharField("Password", max_length=240)
    def __str__(self):
        return self.name