from django.db import models
from cloudinary.models import CloudinaryField
import bcrypt
from datetime import datetime, timedelta
# Create your models here.
class Student(models.Model):
    class OptionEnum(models.TextChoices):
        OPTION1 = '1', 'Accepted'
        OPTION2 = '2', 'Pending'
        OPTION3 = '0', 'Denied'
    name = models.CharField("Name", max_length=240)
    email = models.EmailField(default='')
    password = models.CharField("Password", max_length=240, default='')
    roll = models.CharField("RollNumber", max_length=240, primary_key=True)
    profileImage = CloudinaryField('image',null=True) # for recognition
    idImage = CloudinaryField('image',null=True) # for verification
    requestStatus = models.CharField(max_length=1, choices=OptionEnum.choices, default=OptionEnum.OPTION2)
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, default=None)
    created = models.DateField( default=datetime.now())
    updated= models.DateField( default=datetime.now())
    isActive = models.BooleanField(default=False)
    salt = models.CharField("Salt", default='')
    def __str__(self):
        return self.name
    def setPassword(self, password):
        self.password = bcrypt.hashpw(password.encode('utf8'), self.salt)
    def checkPassword(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

class OTPModel(models.Model):
    email = models.EmailField(default='')
    otp = models.IntegerField(max_length=6, default=None)
    created = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return self.email

class VerifiedEmails(models.Model):
    email = models.EmailField(default='')
    created = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return self.email
    
class Faculty(models.Model):
    name = models.CharField("Name", max_length=240, default='')
    email = models.EmailField(default='')
    password = models.CharField("Password", max_length=240, default='')
    created = models.DateField(default=datetime.now())
    code = models.CharField("Code", max_length=240, primary_key=True)
    courses = models.ManyToManyField('Course', through='BatchCourseFaculty', default=[])
    isActive = models.BooleanField(default=False)
    salt = models.CharField("Salt", default='')
    def __str__(self):
        return self.name    
    def setPassword(self, password):
        self.password = bcrypt.hashpw(password.encode('utf8'), self.salt)
    def checkPassword(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

class Batch(models.Model):
    title = models.CharField("Title", max_length=240, default='')
    code = models.CharField("Code", max_length=240, primary_key=True, default='')
    courses = models.ManyToManyField('Course', through='BatchCourseFaculty', default=[])
    created = models.DateField( default=datetime.now())
    updated = models.DateField( default=datetime.now())
    
class Course(models.Model):
    name = models.CharField("Name", max_length=240,default='')
    code = models.CharField("Code", max_length=240, primary_key=True, default='')
    batches = models.ManyToManyField(Batch, through='BatchCourseFaculty', default=[])
    created = models.DateField( default=datetime.now())
    updated = models.DateField( default=datetime.now())
    def __str__(self):
        return self.name
    
class Codes(models.Model):
    uniqueCode = models.CharField("UniqueCode", max_length=240, primary_key=True, default='')
    isActive = models.BooleanField(default=False)
    created = models.DateField( default=datetime.now())
    updated = models.DateField( default=datetime.now())
    def __str__(self):
        return self.name    

class BatchCourseFaculty(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, default=None)
    created = models.DateField( default=datetime.now())
    updated = models.DateField( default=datetime.now())
    def __str__(self):
        return self.name
    

class Attendance(models.Model):
    BCF_id = models.ForeignKey(BatchCourseFaculty, on_delete=models.CASCADE, default=None)
    roll = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    date = models.DateField( default=datetime.today())
    created = models.DateField( default=datetime.now())
    updated = models.DateField( default=datetime.now())
    def __str__(self):
        return self.name
    
class QRCodeTable(models.Model):
    classRoom = models.CharField("ClassRoom", max_length=240, default='', primary_key=True)
    qrCode = models.CharField("QRCode", max_length=240, default='')
    created = models.DateField( default=datetime.now())
    updated = models.DateField( default=datetime.now())
    def __str__(self):
        return self.name
    

class FacultyCodeStatus(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, default=None)
    classRoom = models.ForeignKey(QRCodeTable, on_delete=models.CASCADE, default=None)
    status = models.BooleanField(default=False)
    lastActivated = models.DateField("LastActivated", default=datetime.now())
    created = models.DateField( default=datetime.now())
    updated = models.DateField( default=datetime.now())
    def __str__(self):
        return self.name
    
    
class Admin(models.Model):
    email = models.EmailField(default='')
    password = models.CharField("Password", max_length=240, default='')
    def __str__(self):
        return self.name