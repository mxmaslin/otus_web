import datetime

from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .mixins import GradeMixin


class Course(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    started = models.DateTimeField(
        verbose_name='Дата начала',
        default=timezone.now,
        validators=[
            MinValueValidator(
                make_aware(datetime.datetime(1970, 1, 1, 0, 0, 0))
            ),
            MaxValueValidator(timezone.now)
        ]
    )
    teacher = models.ForeignKey(
        'profiles.Teacher', verbose_name='Преподаватель', on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.name} {self.started}'

    @property
    def url(self):
        return reverse('courses:course-detail-api', args=[str(self.id)])

    class Meta:
        ordering = 'name',


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=80, verbose_name='Название урока')
    content = models.TextField(verbose_name='Содержание урока')

    def __str__(self):
        return f'{self.course} {self.name}'

    class Meta:
        ordering = 'course',


class LessonGrade(models.Model, GradeMixin):
    student = models.ForeignKey('profiles.Student', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GradeMixin.GRADES)

    def __str__(self):
        return f'{self.grade} {self.student} {self.lesson}'

    class Meta:
        ordering = 'student', 'lesson', 'grade'


class CourseGrade(models.Model, GradeMixin):
    student = models.ForeignKey('profiles.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GradeMixin.GRADES)

    def __str__(self):
        return f'{self.grade} {self.student} {self.course}'

    class Meta:
        ordering = 'student', 'course', 'grade'
