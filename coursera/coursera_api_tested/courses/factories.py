import factory

from .models import Course, Lesson


class CourseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Course


class LessonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Lesson
