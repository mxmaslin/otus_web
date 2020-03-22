from django.db import models
from django.contrib.auth.models import AbstractUser

from .mixins import ProfileMixin


class User(AbstractUser):
    pass


class Passenger(User, ProfileMixin):
    pass


class Driver(User, ProfileMixin):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)


class Car(models.Model):
    vendor = models.CharField(max_length=10)
    model = models.CharField(max_length=20)
    num_seats = models.IntegerField()
    photo = models.ImageField()
