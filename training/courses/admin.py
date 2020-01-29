from django.contrib import admin

from .models import Teacher, Student, Class, Lesson, LessonGrade, ClassGrade


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = 'position', 'first_name', 'last_name'
    list_filter = 'position', 'courses'
    list_display_links = 'position', 'first_name', 'last_name'
    search_fields = 'last_name',


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = 'first_name', 'last_name', 'graduated'
    list_filter = 'courses',
    list_display_links = 'first_name', 'last_name', 'graduated'
    search_fields = 'last_name',


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = 'name', 'started'
    list_filter = 'name',
    list_display_links = 'name', 'started'
    search_fields = 'name',


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = 'learning_class', 'start_time', 'location'
    list_filter = 'learning_class',
    list_display_links = 'learning_class', 'start_time', 'location'


@admin.register(LessonGrade)
class LessonGradeAdmin(admin.ModelAdmin):
    list_display = 'student', 'lesson', 'grade'
    list_filter = 'student', 'grade'
    list_display_links = 'student', 'lesson', 'grade'
    search_fields = 'student',


@admin.register(ClassGrade)
class ClassGradeGradeAdmin(admin.ModelAdmin):
    list_display = 'student', 'course', 'grade'
    list_filter = 'student', 'course', 'grade'
    list_display_links = 'student', 'course', 'grade'
    search_fields = 'student', 'course'
