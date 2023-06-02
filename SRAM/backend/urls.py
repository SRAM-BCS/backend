from django.urls import path
from .views import register, student
urlpatterns = [
	path('register/', register, name='register'),
    path('student/', student, name='student')
 ]
