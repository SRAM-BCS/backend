from django.urls import path
from .views import register, student
urlpatterns = [
	path('register/', register, name='register'),
    path('student/', student, name='student')
    path('faculty/code/status', student, name='student')
    path('admin/student/approve', student, name='student')
 ]
