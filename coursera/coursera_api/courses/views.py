from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.forms.models import modelformset_factory

from .models import Course, Lesson
from .forms import CourseForm, LessonFormSet
from profiles.models import Teacher


class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'courses/course-list.html'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_enrolled'] = user.is_course_student(self.object.id)
        context['teaching'] = user.is_course_teacher(self.object.id)
        context['is_authorized'] = (
                user.is_course_student(self.object.id) or
                user.is_teacher
        )
        return context


def enroll(request, pk):
    course = Course.objects.get(pk=pk)
    request.user.student.courses.add(course)
    return render(request, 'courses/enroll.html', {'course': course})


def leave(request, pk):
    course = Course.objects.get(pk=pk)
    request.user.student.courses.remove(course)
    return render(request, 'courses/leave.html', {'course': course})


class MyCourseListView(ListView):
    model = Course
    context_object_name = 'my_courses'
    template_name = 'courses/my-courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        my_courses = student.courses.all()
        context.update({'student': student, 'my_courses': my_courses})
        return context


class MyLecturingView(ListView):
    model = Course
    context_object_name = 'lecturing_courses'
    template_name = 'courses/lecturing.html'

    def get_teacher(self):
        return Teacher.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'teacher': self.get_teacher()})
        return context

    def get_queryset(self):
        teacher = self.get_teacher()
        if teacher:
            return Course.objects.filter(teacher=teacher.first())
        return Course.objects.none()


def create_course(request):
    form = CourseForm(request.POST or None)
    formset = LessonFormSet(
        request.POST or None,
        queryset=Lesson.objects.none()
    )
    teacher = Teacher.objects.filter(id=request.user.id)
    if form.is_valid() and formset.is_valid():
        course = form.save(commit=False)
        course.teacher = teacher.first()
        course.save()
        lessons = []
        for f_form in formset:
            if f_form.is_valid() and f_form.has_changed():
                lesson_name = f_form.cleaned_data['name']
                lesson_content = f_form.cleaned_data['content']
                lessons.append(
                    Lesson(name=lesson_name, content=lesson_content, course=course)
                )
        Lesson.objects.bulk_create(lessons)
        request.session['course_name'] = form.cleaned_data['name']
        return redirect(reverse('courses:create-success'))
    return render(
        request,
        'courses/create-course.html',
        {'teacher': teacher, 'form': form, 'formset': formset}
    )


def create_success(request):
    course_name = request.session['course_name']
    return render(
        request, 'courses/create-success.html', {'course_name': course_name}
    )


def edit_course(request, pk):
    course = Course.objects.filter(pk=pk)
    form = CourseForm(request.POST or None, instance=course.first())
    extras = 1
    if len(course.first().lessons.all()) > 0:
        extras = 0
    lesson_model_fs_factory = modelformset_factory(
        Lesson, fields=['name', 'content'], extra=extras
    )
    formset = lesson_model_fs_factory(
        request.POST or None,
        queryset=Lesson.objects.filter(course=course.first()),
    )
    teacher = Teacher.objects.filter(id=request.user.id)
    if form.is_valid() and formset.is_valid():
        course = form.save()
        lessons = []
        for f_form in formset:
            if f_form.is_valid():
                lesson_name = f_form.cleaned_data['name']
                lesson_content = f_form.cleaned_data['content']
                lessons.append(
                    Lesson(name=lesson_name, content=lesson_content, course=course)
                )
        course.lessons.all().delete()
        Lesson.objects.bulk_create(lessons)
        request.session['course_name'] = form.cleaned_data['name']
        return redirect(reverse('courses:edit-success'))
    return render(
        request,
        'courses/edit.html',
        {'teacher': teacher, 'course': course, 'form': form, 'formset': formset}
    )


def edit_success(request):
    course_name = request.session['course_name']
    return render(
        request, 'courses/edit-success.html', {'course_name': course_name}
    )


def delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.lessons.all().delete()
    course_name = str(course)
    course.delete()
    return render(request, 'courses/delete.html', {'course_name': course_name})


class LecturingCourseDetailView(DetailView):
    model = Course
    template_name = 'courses/'
