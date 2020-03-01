from rest_framework import serializers

from .models import Course, Lesson


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'name', 'started'


class CourseDetailSerializer(serializers.ModelSerializer):
    teachers = serializers.RelatedField( read_only=True)

    class Meta:
        model = Course
        fields = 'id', 'name', 'started', 'teachers'



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = 'id', 'course', 'started'
