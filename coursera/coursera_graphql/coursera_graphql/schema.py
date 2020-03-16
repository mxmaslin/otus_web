import graphene

from graphql import GraphQLError

from graphene_django.types import DjangoObjectType, ObjectType

from courses.models import Course, Lesson
from profiles.models import Teacher, Student


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher


class StudentType(DjangoObjectType):
    class Meta:
        model = Student


class Query(ObjectType):
    course = graphene.Field(CourseType, id=graphene.Int())
    lesson = graphene.Field(LessonType, id=graphene.Int())
    teacher = graphene.Field(TeacherType, id=graphene.Int())
    student = graphene.Field(StudentType, id=graphene.Int())

    courses = graphene.List(CourseType)
    lessons = graphene.List(LessonType)
    teachers = graphene.List(TeacherType)
    students = graphene.List(StudentType)

    def resolve_course(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                return Course.objects.get(pk=id)
            except Course.DoesNotExist:
                raise GraphQLError(f'Course with {id} not found')
        return None

    def resolve_lesson(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                return Lesson.objects.get(pk=id)
            except Lesson.DoesNotExist:
                raise GraphQLError(f'Lesson with {id} not found')
        return None

    def resolve_teacher(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                return Teacher.objects.get(pk=id)
            except Lesson.DoesNotExist:
                raise GraphQLError(f'Teacher with {id} not found')
        return None

    def resolve_student(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                return Student.objects.get(pk=id)
            except Student.DoesNotExist:
                raise GraphQLError(f'Student with {id} not found')
        return None

    def resolve_courses(self, info, **kwargs):
        return Course.objects.all()

    def resolve_lessons(self, info, **kwargs):
        return Lesson.objects.all()

    def resolve_teachers(self, info, **kwargs):
        return Teacher.objects.all()

    def resolve_students(self, info, **kwargs):
        return Student.objects.all()


class TeacherInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()


class CourseInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    started = graphene.DateTime()
    teacher = graphene.String()


class CreateCourse(graphene.Mutation):
    class Arguments:
        course_data = CourseInput(required=True)

    course = graphene.Field(CourseType)
    ok = graphene.Boolean()

    def mutate(self, info, course_data):
        teacher_obj = Teacher.objects.filter(
            username=course_data.pop('teacher')
        ).first()
        if not teacher_obj:
            raise GraphQLError(f'Teacher {course_data.teacher} does not exist')
        course = Course.objects.create(**course_data, teacher=teacher_obj)
        return CreateCourse(course=course, ok=True)


class UpdateCourse(graphene.Mutation):
    class Arguments:
        course_data = CourseInput(required=True)

    course = graphene.Field(CourseType)
    ok = graphene.Boolean()

    def mutate(self, info, course_data):
        course = Course.objects.get(pk=course_data.id)
        name = course_data.name
        started = course_data.started
        teacher_obj = Teacher.objects.filter(
            username=course_data.pop('teacher')
        ).first()
        if not teacher_obj:
            raise GraphQLError(f'Teacher {course_data.teacher} does not exist')
        course.name = name
        course.started = started
        course.teacher = teacher_obj
        course.save()
        return UpdateCourse(course=course, ok=True)


class Mutation(ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
