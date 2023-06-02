from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField()
    roll = models.CharField("RollNumber", max_length=240, primary_key=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name