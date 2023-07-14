from django.urls import path
from .views import pending_student_status, save_student_status, save_new_admin, get_all_admins, QR, forgot_password, batch, course, faculty, admin_login

urlpatterns = [
    path('new',save_new_admin,name="SaveNewAdmin"),
	
    #STUDENT
    path('student/status/pending', pending_student_status, name='GetPendingStudentStatus'),
    path('student/status/modify', save_student_status, name='ChangeStudentStatus'),
    
    #QR
    path('qr/generate', QR, name='generateQR'),
    path('qr', QR, name='getClassQR'),
    
    #BATCH
    path('batch/new', batch, name='SaveNewBatch'),
    path('batch/all', batch, name='GetAllBatches'),
    
    #COURSE
    path('course/new', course, name='SaveNewCourse'),
    path('course/all', course, name='GetAllCourses'),
    
    #FACULTY
    path('faculty/new', faculty, name='SaveNewFaculty'),
    path('faculty/all', faculty, name='GetAllFaculties'),

    # ADMIN
    path('forgot/password', forgot_password, name='ForgotPassword'),
    path('get/', get_all_admins, name='GetAllAdmins'),
    path('login/', admin_login, name='AdminLogin'),
    # #CLASSROOM
    # path("classroom/new", classroom, name="SaveNewClassroom"),
 ]
