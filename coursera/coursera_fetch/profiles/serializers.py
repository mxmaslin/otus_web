from rest_framework import serializers

from .models import Student, Teacher


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['username', 'password', 'first_name', 'last_name']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['username', 'password', 'first_name', 'last_name']

