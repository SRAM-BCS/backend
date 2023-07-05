from django.urls import path
from .views import pending_student_status, save_student_status

urlpatterns = [
	path('student/status/pending', pending_student_status, name='GetPendingStudentStatus'),
    path('student/status/modify', save_student_status, name='ChangeStudentStatus')
 ]
