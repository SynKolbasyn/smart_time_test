from http import HTTPStatus
from json import dumps

from django.test import Client, TestCase
from parameterized import parameterized

from api.models import Exam, Room, Subject, User


class RegisterTests(TestCase):
    def setUp(self):
        User.objects.create(email="student.1@edu.hse.ru", password="12345678")

    @parameterized.expand(
        [
            (
                "student.1@edu.hse.ru",
                "1234",
                HTTPStatus.BAD_REQUEST,
            ),
            (
                "student.1",
                "12345678",
                HTTPStatus.BAD_REQUEST,
            ),
            (
                "student.1@edu.hse.ru",
                "12345678",
                HTTPStatus.BAD_REQUEST,
            ),
            (
                "student.2@edu.hse.ru",
                "12345678",
                HTTPStatus.OK,
            ),
        ]
    )
    def test_insertion(self, email, password, http_status):
        data = {"email": email, "password": password}
        response = Client().post(
            "/api/register/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, http_status)


class ExamRegistrationsTests(TestCase):
    def setUp(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
        }
        response = Client().post(
            "/api/register/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        subject = Subject.objects.create(subject_name="math")
        room = Room.objects.create(room_number=101)
        Exam.objects.create(subject_id=subject, room_id=room)

    def test_email_is_not_valid(self):
        data = {
            "email": "studentedu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 101,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_subject_is_not_valid(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": ["math"],
            "room_number": 101,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_room_is_not_valid(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": [101],
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_registrarion_success(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 101,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ExamUnregistrationsTests(TestCase):
    def setUp(self):
        user = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
        }
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 101,
        }
        response = Client().post(
            "/api/register/", dumps(user), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        subject = Subject.objects.create(subject_name="math")
        room = Room.objects.create(room_number=101)
        Exam.objects.create(subject_id=subject, room_id=room)
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unregister_success(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 101,
        }
        response = Client().delete(
            "/api/unregister_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
