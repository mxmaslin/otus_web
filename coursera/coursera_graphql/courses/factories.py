import factory

from .models import Course, Lesson
from profiles.models import Teacher


class CourseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Course


class LessonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Lesson


class TeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Teacher
