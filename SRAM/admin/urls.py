from django.urls import path
from .views import pending_student_status, save_student_status, save_new_admin, QR

urlpatterns = [
    path('new',save_new_admin,name="SaveNewAdmin"),
	path('student/status/pending', pending_student_status, name='GetPendingStudentStatus'),
    path('student/status/modify', save_student_status, name='ChangeStudentStatus'),
    path('qr/generate', QR, name='generateQR'),
    path('qr', QR, name='getClassQR')
    
 ]
