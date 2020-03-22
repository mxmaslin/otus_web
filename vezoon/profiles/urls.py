from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'profiles'

urlpatterns = [
    # path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
