from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knox.models import AuthToken

from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    UserSerializer,
    CreateStudentSerializer,
    CreateTeacherSerializer,
    LoginSerializer
)


@api_view(['POST'])
def register_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateStudentView(generics.GenericAPIView):
    serializer_class = CreateStudentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        _, token = AuthToken.objects.create(student)
        return Response({
            "student": StudentSerializer(
                student, context=self.get_serializer_context()
            ).data,
            "token": token
        })


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class CreateTeacherView(generics.GenericAPIView):
    serializer_class = CreateTeacherSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        _, token = AuthToken.objects.create(teacher)
        return Response({
            "teacher": TeacherSerializer(
                teacher, context=self.get_serializer_context()
            ).data,
            "token": token
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "student": StudentSerializer(
                user, context=self.get_serializer_context()
            ).data,
            "token": token
        })


class StudentView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = StudentSerializer

    def get_object(self):
        return self.request.user


class TeacherView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TeacherSerializer

    def get_object(self):
        return self.request.user