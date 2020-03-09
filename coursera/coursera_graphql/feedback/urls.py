from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('thanks/', views.thanks, name='thanks'),
    path('', views.FeedbackView.as_view(), name='feedback'),
]
