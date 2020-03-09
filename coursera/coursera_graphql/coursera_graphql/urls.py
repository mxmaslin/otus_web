from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Coursera API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('feedback/', include('feedback.urls', namespace='feedback')),

    path('api/', include('courses.urls', namespace='courses-api')),
    path('token-auth-api/',
         include('token_auth_api.urls', namespace='token-auth-api')
         ),
    path('profiles-api/', include('profiles.urls', namespace='profiles-api')),

    path('swagger/', schema_view),

    path('', include('courses.urls', namespace='courses')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
