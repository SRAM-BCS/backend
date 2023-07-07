from django.urls import path
from .views import facultyCode
urlpatterns = [
    path('code/status', facultyCode, name='faculty/code'),
 ]
