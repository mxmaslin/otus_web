from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Passenger(User):
    pass
# email, телефон, first_name, last_name, фото, **оценки**


class Driver(User):
    pass
# email, телефон, first_name, last_name, фото, **оценки **, **автомобиль**

