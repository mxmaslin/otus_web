from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('index/', views.index, name='index'),
]
