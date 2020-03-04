from django.http import Http404

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Course
from .serialilzers import (
    CourseListSerializer,
    CoursePublicDetailSerializer,
    CourseStudentDetailSerializer,
    CourseTeacherSerializer
)
from .permissions import IsTeacherOrReadOnly, IsCourseTeacherOrReadOnly

from profiles.models import User

class CourseList(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseTeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):
    permission_classes = [IsCourseTeacherOrReadOnly]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CoursePublicDetailSerializer(course)
        if request.user.is_authenticated:
            enrolled = request.user.is_course_student(pk)
            teacher = request.user.is_teacher
            if enrolled or teacher:
                serializer = CourseStudentDetailSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        course = self.get_object(pk)
        self.check_object_permissions(self.request, course)
        serializer = CourseTeacherSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        course = self.get_object(pk)
        self.check_object_permissions(self.request, course)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses(request):
    try:
        courses = request.user.student.courses
    except (User.student.RelatedObjectDoesNotExist, ):
        raise serializers.ValidationError(
            'Ошибка получения курсов студента'
            )
    serializer = CourseStudentDetailSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lecturing(request):
    try:
        courses = Course.objects.filter(teacher=request.user.teacher)
    except (User.teacher.RelatedObjectDoesNotExist, ):
        raise serializers.ValidationError(
            'Ошибка получения курсов преподавателя'
            )
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def register_student(request):
    pass


@api_view(['POST'])
def register_teacher(request):
    pass


@api_view(['GET'])
def enroll_api(request):
    pass


@api_view(['GET'])
def leave_api(request):
    pass

