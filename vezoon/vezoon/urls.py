from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Vezoon API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('trips/', include('trips.urls', namespace='trips')),
    path('communications/', include('communications.urls', namespace='communications')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
