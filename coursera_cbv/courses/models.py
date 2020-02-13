import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Course(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    started = models.PositiveIntegerField(
        default=datetime.date.today().year,
        validators=[
            MinValueValidator(1970),
            max_value_current_year
        ],
        verbose_name='Дата начала'
    )

    def __str__(self):
        return f'{self.name} {self.started}'

    class Meta:
        ordering = 'name',


class Lesson(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=80, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    content = models.TextField()

    def __str__(self):
        return f'{self.course} {self.start_time}'

    class Meta:
        ordering = 'course', '-start_time'


class LessonGrade(models.Model):
    A_GRADE = 'A'
    B_GRADE = 'B'
    C_GRADE = 'C'
    D_GRADE = 'D'
    GRADES = (
        (A_GRADE, 'Excellent'),
        (B_GRADE, 'Good'),
        (C_GRADE, 'Fair'),
        (D_GRADE, 'Poor'),
    )
    student = models.ForeignKey('profiles.Student', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADES)

    def __str__(self):
        return f'{self.grade} {self.student} {self.lesson}'

    class Meta:
        ordering = 'student', 'lesson', 'grade'


class CourseGrade(models.Model):
    A_GRADE = 'A'
    B_GRADE = 'B'
    C_GRADE = 'C'
    D_GRADE = 'D'
    GRADES = (
        (A_GRADE, 'Excellent'),
        (B_GRADE, 'Good'),
        (C_GRADE, 'Fair'),
        (D_GRADE, 'Poor'),
    )
    student = models.ForeignKey('profiles.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADES)

    def __str__(self):
        return f'{self.grade} {self.student} {self.course}'

    class Meta:
        ordering = 'student', 'course', 'grade'
