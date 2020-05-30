from django.contrib import admin

from .models import Course, Lesson, LessonGrade, CourseGrade


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = 'name', 'started'
    list_filter = 'name',
    list_display_links = 'name', 'started'
    search_fields = 'name',


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = 'course', 'name'
    list_filter = 'course',
    list_display_links = 'course', 'name'


@admin.register(LessonGrade)
class LessonGradeAdmin(admin.ModelAdmin):
    list_display = 'student', 'lesson', 'grade'
    list_filter = 'student', 'grade'
    list_display_links = 'student', 'lesson', 'grade'
    search_fields = 'student',


@admin.register(CourseGrade)
class ClassGradeGradeAdmin(admin.ModelAdmin):
    list_display = 'student', 'course', 'grade'
    list_filter = 'student', 'course', 'grade'
    list_display_links = 'student', 'course', 'grade'
    search_fields = 'student', 'course'
