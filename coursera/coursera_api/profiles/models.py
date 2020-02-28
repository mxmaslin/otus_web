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
    @property
    def is_student(self):
        return Student.objects.filter(id=self.id).exists()

    @property
    def is_teacher(self):
        return Teacher.objects.filter(id=self.id).exists()

    @property
    def student(self):
        if self.is_student:
            return Student.objects.get(id=self.id)
        return None


class Teacher(User, SendMailMixin):
    courses = models.ManyToManyField(
        'courses.Course', related_name='teachers', blank=True
    )

    def is_course_teacher(self, course_id):
        return self.courses.filter(id=course_id).exists()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = 'last_name',


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

    def is_enrolled(self, course_id):
        return self.courses.filter(id=course_id).exists()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = '-graduated', 'last_name'
