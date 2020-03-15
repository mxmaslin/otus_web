import sys
import logging
import unittest
import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import (
    force_authenticate, APITestCase, APIRequestFactory, APITransactionTestCase,
    APISimpleTestCase
)
from rest_framework.authtoken.models import Token
from graphene.test import Client as GrapheneClient

from .factories import CourseFactory, LessonFactory
from .api_views import CourseDetail, leave
from profiles.models import Teacher, Student

from coursera_graphql import schema


class SetupMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    @classmethod
    def setUpTestData(cls):
        cls.teacher1 = Teacher.objects.create_user('teacher1', password='123')
        cls.teacher2 = Teacher.objects.create_user('teacher2', password='123')
        cls.student1 = Student.objects.create_user('student1', password='123')
        cls.student2 = Student.objects.create_user('student2', password='123')
        cls.teacher1token = Token.objects.create(user=cls.teacher1)
        cls.teacher2token = Token.objects.create(user=cls.teacher2)
        cls.student1token = Token.objects.create(user=cls.student1)
        cls.student2token = Token.objects.create(user=cls.student2)

    def setUp(self):
        self.course1 = CourseFactory(
            name='Курс1',
            started='2017-05-01T15:12:04+03:00',
            teacher=self.teacher1,
        )
        self.course2 = CourseFactory(
            name='Курс2',
            started='2018-06-01T15:12:04+03:00',
            teacher=self.teacher2,
        )
        self.lesson1 = LessonFactory(
            name='Название урока1',
            content='Содержание урока1',
            course=self.course1
        )
        self.lesson2 = LessonFactory(
            name='Название урока2',
            content='Содержание урока2',
            course=self.course2
        )
        self.course_post_payload = {
            'name': 'Тестовый курс',
            'started': '2017-05-01T15:12:04+03:00',
            'teacher': self.teacher1.username,
            'lessons': [
                {
                    'name': 'Название тестового урока',
                    'content': 'Содержание тестового урока'
                }
            ]
        }
        self.course_put_payload = {
            'name': 'Изменённый тестовый курс',
            'started': '2017-05-01T15:12:04+03:00',
            'teacher': self.teacher1.username,
            'lessons': [
                {
                    'name': 'Изменённое название тестового урока',
                    'content': 'Изменённое содержание тестового урока'
                }
            ]
        }


class TestCaseForCourseAPITransaction(SetupMixin, APITransactionTestCase):
    def setUp(self):
        super().setUpTestData()
        super().setUp()

    def test_course_details_enrolled(self):
        self.student1.courses.add(self.course1)
        factory = APIRequestFactory()
        course = self.course1
        view = CourseDetail.as_view()
        request = factory.get('/v1/course/')
        force_authenticate(request, user=self.student1, token=self.student1token)
        response = view(request, pk=course.id)
        self.assertTrue('lessons' in response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_enrolled(self):
        self.student1.courses.add(self.course1)
        factory = APIRequestFactory()
        course = self.course1
        view = CourseDetail.as_view()
        request = factory.get('/v1/course/')
        force_authenticate(request, user=self.student1, token=self.student1token)
        response = view(request, pk=course.id)
        self.assertTrue(response.data['name'] == 'Курс1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_course_student(self):
        self.student1.courses.add(self.course1)
        factory = APIRequestFactory()
        course = self.course1
        view = leave
        payload = {
            'course_id': course.id,
            'student_username': self.student1.username
        }
        request = factory.post('/v1/leave/', payload)
        force_authenticate(request, user=self.student1, token=self.student1token)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCaseForCourseAPISimple(SetupMixin, APISimpleTestCase):
    def setUp(self):
        super(SetupMixin, self).setUp()

    def test_my_enrolled_anon(self):
        courses_url = reverse('courses:my-courses-api')
        response = self.client.get(courses_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_my_lecturing_anon(self):
        courses_url = reverse('courses:lecturing-api')
        response = self.client.get(courses_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCaseForCourseAPI(SetupMixin, APITestCase):
    def test_course_post_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher1token.key)
        courses_url = reverse('courses:course-list-api')
        response = self.client.post(courses_url, self.course_post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_post_student(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student1token.key)
        courses_url = reverse('courses:course-list-api')
        response = self.client.post(courses_url, self.course_post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_post_anon(self):
        courses_url = reverse('courses:course-list-api')
        response = self.client.post(courses_url, self.course_post_payload,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_list(self):
        course1 = self.course1
        course2 = self.course2
        courses_url = reverse('courses:course-list-api')
        response = self.client.get(courses_url)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_details_teacher(self):
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher1token.key)
        response = self.client.get(courses_url)
        self.assertTrue('lessons' in response.json())

    def test_course_details_anon(self):
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        response = self.client.get(courses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_put_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher1token.key)
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        response = self.client.put(courses_url, self.course_put_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_other_put_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher2token.key)
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        response = self.client.put(courses_url, self.course_put_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_put_student(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student1token.key)
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        response = self.client.put(courses_url, self.course_put_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_put_anon(self):
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        response = self.client.put(courses_url, self.course_put_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_my_lecturing(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher1token.key)
        courses_url = reverse('courses:lecturing-api')
        response = self.client.get(courses_url, format='json')
        self.assertTrue(response.json()[0]['name'] == 'Курс1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_lecturing_student(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student1token.key)
        courses_url = reverse('courses:lecturing-api')
        response = self.client.get(courses_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



#
# @pytest.fixture
# def get_course():
#
#     return
#
#
# def test_hey():
#     client = GrapheneClient(my_schema)
#     executed = client.execute('''{ hey }''')
#     assert executed == {
#         'data': {
#             'hey': 'hello!'
#         }
#     }
