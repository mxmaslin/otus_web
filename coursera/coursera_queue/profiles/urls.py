from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('student-signup/', views.StudentSignUp.as_view(), name='student-signup'),
    path('teacher-signup/', views.TeacherSignUp.as_view(), name='teacher-signup'),
]
