from django.urls import path

from . import views

app_name = 'token_auth_api'

urlpatterns = [
    path('login/', views.login, name='login'),
]
