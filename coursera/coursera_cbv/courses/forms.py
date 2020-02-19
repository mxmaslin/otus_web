from django import forms
from django.forms.models import modelformset_factory

from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = 'name', 'started'


LessonFormSet = modelformset_factory(Lesson, fields=['name', 'content'])
