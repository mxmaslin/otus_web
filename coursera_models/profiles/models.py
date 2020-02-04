import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .mixins import SendMailMixin


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class User(AbstractUser):
    pass


class Teacher(User, SendMailMixin):
    POSTGRADUATE = 'PG'
    ASSOCIATE_PROFESSOR = 'AP'
    HEAD_OF_DEPARTMENT = 'HD'
    POSITIONS = (
        (POSTGRADUATE, 'Postgraduate'),
        (ASSOCIATE_PROFESSOR, 'Associate Professor'),
        (HEAD_OF_DEPARTMENT, 'Head of Departament'),
    )
    position = models.CharField(
        max_length=2, choices=POSITIONS, default=POSTGRADUATE
    )
    courses = models.ManyToManyField(
        'courses.Course', related_name='teachers', blank=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = 'position', 'last_name'


class Student(User, SendMailMixin):
    graduated = models.PositiveIntegerField(
        default=datetime.date.today().year,
        validators=[
            MinValueValidator(1970),
            max_value_current_year
        ]
    )
    courses = models.ManyToManyField(
        'courses.Course', related_name='students', blank=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = '-graduated', 'last_name'
