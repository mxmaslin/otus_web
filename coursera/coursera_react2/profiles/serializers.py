from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import Student, Teacher, User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['username', 'password', 'first_name', 'last_name']


class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        student = Student.objects.create_user(
            username=validated_data['username'],
            email=None,
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return student


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['username', 'password', 'first_name', 'last_name']


class CreateTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        teacher = Teacher.objects.create_user(
            username=validated_data['username'],
            email=None,
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return teacher


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            'Unable to log in with provided credentials'
        )


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_student = serializers.BooleanField()
    is_teacher = serializers.BooleanField()
    student = StudentSerializer()
    teacher = TeacherSerializer()
