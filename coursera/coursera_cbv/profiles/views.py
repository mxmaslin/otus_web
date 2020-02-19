from django.urls import reverse_lazy
from django.views import generic

from .forms import StudentSignUpForm, TeacherSignUpForm


class StudentSignUp(generic.CreateView):
    form_class = StudentSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'student-signup.html'


class TeacherSignUp(generic.CreateView):
    form_class = TeacherSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'teacher-signup.html'
