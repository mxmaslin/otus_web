from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('django.contrib.auth.urls')),
    re_path('^', include('courses.urls', namespace='courses')),
]
