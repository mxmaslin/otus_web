from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Teacher, Student


class TeacherCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Teacher
        fields = 'username', 'first_name', 'last_name', 'password'


class TeacherChangeForm(UserChangeForm):
    class Meta:
        model = Teacher
        fields = 'username', 'first_name', 'last_name', 'password'


class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Student
        fields = 'graduated', 'courses'


class StudentChangeForm(UserChangeForm):
    class Meta:
        model = Student
        fields = 'graduated', 'courses'


class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = Student
        fields = 'username', 'first_name', 'last_name', 'password1', 'password2'


class TeacherSignUpForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = 'username', 'first_name', 'last_name', 'password1', 'password2'
