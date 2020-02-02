from django.contrib import admin

from .models import Teacher, Student


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = 'username', 'password', 'position', 'first_name', 'last_name'
    list_display = 'position', 'first_name', 'last_name'
    list_filter = 'position', 'courses'
    list_display_links = 'position', 'first_name', 'last_name'
    search_fields = 'last_name',


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = 'username', 'password', 'first_name', 'last_name', 'graduated'
    list_display = 'first_name', 'last_name', 'graduated'
    list_filter = 'courses',
    list_display_links = 'first_name', 'last_name', 'graduated'
    search_fields = 'last_name',
