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


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = 'id', 'course', 'name', 'content'


class CourseStudentDetailSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = 'id', 'name', 'started', 'teacher', 'lessons'
