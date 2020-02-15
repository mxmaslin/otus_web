from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('enroll/<int:pk>/', views.enroll, name='enroll'),
    path('leave/<int:pk>/', views.leave, name='leave'),
    path('my-courses/', views.MyCourseListView.as_view(), name='my-courses'),
    path('lecturing/', views.MyLecturingView.as_view(), name='lecturing'),
    path('create/', views.create_course, name='create'),
    path('edit/<int:pk>/', views.edit_course, name='edit'),
    path('create-success/', views.create_success, name='create-success'),
    path('', views.CourseListView.as_view(), name='course-list'),
]
