from rest_framework import serializers

from .models import Course, Lesson

from profiles.models import Teacher


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'name', 'started', 'url'


class CoursePublicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'name', 'started'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = 'id', 'course', 'name', 'content'


class LessonCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Lesson
        fields = 'id', 'name', 'content'


class CourseStudentDetailSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = 'id', 'name', 'started', 'teacher', 'lessons'


class CourseTeacherSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=False, trim_whitespace=True)
    started = serializers.DateTimeField()
    teacher = serializers.CharField(allow_blank=False, trim_whitespace=True)
    lessons = LessonCreateSerializer(many=True)

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons')
        teacher = validated_data.pop('teacher')
        try:
            teacher = Teacher.objects.get(username=teacher)
        except (Teacher.DoesNotExist, ):
            raise serializers.ValidationError(
                f'Учитель с username {teacher} отсутствует'
            )
        course = Course.objects.create(teacher=teacher, **validated_data)
        for lesson_data in lessons_data:
            Lesson.objects.create(course=course, **lesson_data)
        return course

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.started = validated_data.get('started', instance.started)
        teacher = validated_data.get('teacher', instance.teacher)
        try:
            teacher_obj = Teacher.objects.get(username=teacher)
        except (Teacher.DoesNotExist, ):
            raise serializers.ValidationError(
                f'Учитель с username {teacher} отсутствует'
            )
        instance.teacher = teacher_obj
        instance.save()
        lessons = validated_data.get('lessons', instance.lessons)
        new_lessons_ids = []
        for lesson in lessons:
            lesson_obj, created = Lesson.objects.get_or_create(
                id=lesson.get('id'), course=instance
            )
            lesson_obj.name = lesson.get('name')
            lesson_obj.content = lesson.get('content')
            lesson_obj.save()
            new_lessons_ids.append(lesson_obj.id)
        Lesson.objects.filter(course=instance).exclude(id__in=new_lessons_ids).delete()
        return instance
