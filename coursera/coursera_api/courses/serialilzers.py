from rest_framework import serializers

from .models import Course, Lesson


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'name', 'started', 'url'


class CoursePublicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'name', 'started'


class CourseStudentDetailSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')

    class Meta:
        model = Course
        fields = 'id', 'name', 'started', 'teacher'



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = 'id', 'course', 'name'
