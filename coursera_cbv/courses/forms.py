from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory

from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = 'name', 'started'


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = 'name', 'content'


LessonFormSet = modelformset_factory(Lesson, form=LessonForm)


# class LessonForm(forms.ModelForm):
#     class Meta:
#         model = Lesson
#         fields = 'start_time', 'duration', 'location', 'course'
#
#
#     def __init__(self, n=5, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(0, n):
#             self.fields["field_name% d" % i] = forms.CharField()
#
#
# CourseFormSet = formset_factory(form=CourseForm)


# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = 'name', 'started'
    # name = forms.CharField(required=True)
    # started = forms.DateField(
    #     initial=datetime.date.today().year,
    #     validators=[
    #         MinValueValidator(1970),
    #         max_value_current_year
    #     ]
    # )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     lessons = Lesson.objects.filter(course=self.instance)
    #     for i in range(1, len(lessons) + 2):
    #         self.fields[f'start_time_lesson_{i}'] = forms.DateTimeField(
    #             input_formats=['%d/%m/%Y %H:%M'],
    #             widget=forms.DateTimeInput()
    #         )
    #         self.fields[f'duration_lesson_{i}'] = forms.IntegerField(
    #             required=False)
    #         self.fields[f'location_lesson_{i}'] = forms.CharField(
    #             required=False)
    #         self.fields[f'content_lesson_{i}'] = forms.CharField(
    #             widget=forms.Textarea)

        # interests = ProfileInterest.objects.filter(
        #     profile=self.instance
        # )
        # for i in range(len(interests) + 1):
        #     field_name = 'interest_%s' % (i,)
        #     self.fields[field_name] = forms.CharField(required=False)
        #     try:
        #         self.initial[field_name] = interests[i].interest
        #     except IndexError:
        #         self.initial[field_name] = “”
        # # create an extra blank field
        # field_name = 'interest_%s' % (i + 1,)
        # self.fields[field_name] = forms.CharField(required=False)
    #
    # def clean(self):
    #     interests = set()
    #     i = 0
    #     field_name = 'interest_%s' % (i,)
    #     while self.cleaned_data.get(field_name):
    #        interest = self.cleaned_data[field_name]
    #        if interest in interests:
    #            self.add_error(field_name, 'Duplicate')
    #        else:
    #            interests.add(interest)
    #        i += 1
    #        field_name = 'interest_%s' % (i,)
    #    self.cleaned_data[“interests”] = interests
    #
    # def save(self):
    #     profile = self.instance
    #     profile.first_name = self.cleaned_data[“first_name”]
    #     profile.last_name = self.cleaned_data[“last_name”]
    #
    #     profile.interest_set.all().delete()
    #     for interest in self.cleaned_data[“interests”]:
    #        ProfileInterest.objects.create(
    #            profile=profile,
    #            interest=interest,
    #        )

