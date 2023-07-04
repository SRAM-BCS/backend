from django.urls import path
from .views import facultyCode
urlpatterns = [
    path('faculty/code/status', facultyCode, name='faculty/code'),
 ]
