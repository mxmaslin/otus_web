from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles.models import Teacher, Student
from .factories import CourseFactory, LessonFactory


class TestCaseForCourse(APITestCase):
    def setUp(self):
        self.teacher1 = Teacher.objects.create_user('teacher1', password='123')
        self.teacher2 = Teacher.objects.create_user('teacher2', password='123')
        self.student1 = Student.objects.create_user('student1', password='123')
        self.student2 = Student.objects.create_user('student2', password='123')
        self.teacher1token = Token.objects.create(user=self.teacher1)
        self.teacher2token = Token.objects.create(user=self.teacher2)
        self.student1token = Token.objects.create(user=self.student1)
        self.student2token = Token.objects.create(user=self.student2)
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

    def setUpTestData(self):
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
        response = self.client.post(courses_url, self.course_post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_list(self):
        course1 = self.course1
        course2 = self.course2
        courses_url = reverse('courses:course-list-api')
        response = self.client.get(courses_url)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_details_anon(self):
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        response = self.client.get(courses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_details_enrolled(self):
        self.student1.courses.add(self.course1)
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student1token.key)
        response = self.client.get(courses_url)
        self.assertTrue('lessons' in response.json())

    def test_course_details_teacher(self):
        self.course1.teacher = self.teacher1
        courses_url = reverse('courses:course-detail-api', args=[self.course1.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher1token.key)
        response = self.client.get(courses_url)
        self.assertTrue('lessons' in response.json())

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

    def test_my_enrolled(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student1token.key)
        self.student1.courses.add(self.course1)
        courses_url = reverse('courses:my-courses-api')
        response = self.client.get(courses_url, format='json')
        self.assertTrue(response.json()[0]['name'] == 'Курс1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_enrolled_anon(self):
        courses_url = reverse('courses:my-courses-api')
        response = self.client.get(courses_url, format='json')
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

    def test_my_lecturing_anon(self):
        courses_url = reverse('courses:lecturing-api')
        response = self.client.get(courses_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_leave_course_student(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student1token.key)
        self.student1.courses.add(self.course1)
        courses_url = reverse('courses:leave-api')
        payload = {'course_id': self.course1.id, 'student_username': self.student1.username}
        response = self.client.post(courses_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

