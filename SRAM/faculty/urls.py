from django.urls import path
from .views import facultyCode, forgotPassword, login, getFaculty, facultyBatchCourse
urlpatterns = [
    path('code/status', facultyCode, name='facultyCode'),
    path('forgot/password', forgotPassword, name='forgotPassword'),
    path('login', login, name='login'),
    path('get', getFaculty, name='getFaculty'),
    path('batch/course',facultyBatchCourse,name="associateBatchCourse")
 ]
