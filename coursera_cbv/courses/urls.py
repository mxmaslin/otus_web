from django.urls import path, re_path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='all'),
]
