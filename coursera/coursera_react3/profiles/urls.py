from django.urls import path

from knox.views import LogoutView

from . import views, api_views

app_name = 'profiles'

urlpatterns = [
    path('student-signup/', views.StudentSignUp.as_view(), name='student-signup'),
    path('teacher-signup/', views.TeacherSignUp.as_view(), name='teacher-signup'),

    path('v1/register-student/', api_views.register_student,
         name='register-student-api'),
    path('v1/register-teacher/', api_views.register_teacher,
         name='register-teacher-api'),

    path('v2/register-student/', api_views.CreateStudentView.as_view()),
    path('v2/register-teacher/', api_views.CreateTeacherView.as_view()),

    path('v2/login/', api_views.LoginView.as_view()),
    path('v2/logout/', LogoutView.as_view(), name='knox_logout'),
    path('v2/user/', api_views.get_user),

    path('v2/student/', api_views.StudentView.as_view()),
    path('v2/teacher/', api_views.TeacherView.as_view()),
]
