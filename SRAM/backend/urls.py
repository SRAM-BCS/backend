from django.urls import path
from .views import register, student, login, student_with_email, mark_attendance, get_student_attendance, generate_otp, verify_otp, forgot_password, course
urlpatterns = [
	path('register/', register, name='register'),
    path('get/all/', student, name='student'),
    path('login', login, name='login'),
    path('get/', student_with_email, name='student_with_email'),
    path('course', course, name='student_courses'), # get all courses for a student
    path('attendance', mark_attendance, name='mark_attendance'),
    path('attendance/', get_student_attendance, name='get_student_attendance'),
    path('otp/generate/', generate_otp, name='generate_otp'),
    path('otp/verify/', verify_otp, name='verify_otp'),
    path('forgot/password/', forgot_password, name='forgot_password'),
 ]
