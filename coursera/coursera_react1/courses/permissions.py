from rest_framework import permissions


SAFE_METHODS = ['GET']


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_teacher


class IsCourseTeacherOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated and
                request.user.is_teacher and
                obj.teacher == request.user.teacher
                )


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_student


class IsCourseStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        course_id = request.data['course_id']
        return request.user.is_course_student(course_id)
