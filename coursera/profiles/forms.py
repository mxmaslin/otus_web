from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Teacher, Student


class TeacherCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Teacher
        fields = 'position', 'courses'


class TeacherChangeForm(UserChangeForm):
    class Meta:
        model = Teacher
        fields = 'position', 'courses'


class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Student
        fields = 'graduated', 'courses'


class StudentChangeForm(UserChangeForm):
    class Meta:
        model = Student
        fields = 'graduated', 'courses'
