from django.urls import path

from . import views, api_views

app_name = 'profiles'

urlpatterns = [
    path('student-signup/', views.StudentSignUp.as_view(), name='student-signup'),
    path('teacher-signup/', views.TeacherSignUp.as_view(), name='teacher-signup'),

    path('v1/register-student/', api_views.register_student,
         name='register-student-api'),
    path('v1/register-teacher/', api_views.register_teacher,
         name='register-teacher-api'),
]
