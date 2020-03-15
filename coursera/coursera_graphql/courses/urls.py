from django.urls import path

from . import views, api_views

app_name = 'courses'

urlpatterns = [
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('enroll/<int:pk>/', views.enroll, name='enroll'),
    path('leave/<int:pk>/', views.leave, name='leave'),
    path('my-courses/', views.MyCourseListView.as_view(), name='my-courses'),
    path('lecturing/', views.MyLecturingView.as_view(), name='lecturing'),
    path('create/', views.create_course, name='create'),
    path('create-success/', views.create_success, name='create-success'),
    path('edit/<int:pk>/', views.edit_course, name='edit'),
    path('edit-success/', views.edit_success, name='edit-success'),
    path('delete/<int:pk>/', views.delete, name='delete'),

    path('v1/courses/', api_views.CourseList.as_view(),
         name='course-list-api'),
    path('v1/course/<int:pk>/', api_views.CourseDetail.as_view(),
         name='course-detail-api'),
    path('v1/my-courses/', api_views.my_courses, name='my-courses-api'),
    path('v1/lecturing/', api_views.lecturing, name='lecturing-api'),

    path('v1/enroll/', api_views.enroll, name='enroll-api'),
    path('v1/leave/', api_views.leave, name='leave-api'),

    path('', views.CourseListView.as_view(), name='course-list'),
]
