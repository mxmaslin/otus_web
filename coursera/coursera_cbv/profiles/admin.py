from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import TeacherCreationForm, TeacherChangeForm, StudentCreationForm, \
    StudentChangeForm
from .models import Teacher, Student


class TeacherAdmin(UserAdmin):
    add_form = TeacherCreationForm
    form = TeacherChangeForm
    model = Teacher
    list_display = 'first_name', 'last_name'
    list_filter = 'courses',
    fieldsets = (
        (None, {
            'fields': (
                'username', 'password', 'first_name', 'last_name', 'courses'
            )
        }),
        ('Permissions', {'fields': ('is_active', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'courses')
        }),
    )
    list_display_links = 'first_name', 'last_name'
    search_fields = 'last_name',


admin.site.register(Teacher, TeacherAdmin)


class StudentAdmin(UserAdmin):
    add_form = StudentCreationForm
    form = StudentChangeForm
    model = Student
    list_display = 'graduated', 'first_name', 'last_name'
    list_filter = 'courses',
    fieldsets = (
        (None, {
            'fields': (
                'username', 'password', 'graduated', 'courses', 'first_name', 'last_name'
            )
        }),
        ('Permissions', {'fields': ('is_active', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'graduated', 'courses')}),
    )
    list_display_links = 'first_name', 'last_name', 'graduated'
    search_fields = 'last_name',


admin.site.register(Student, StudentAdmin)
