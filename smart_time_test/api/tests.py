from http import HTTPStatus
from json import dumps

from django.test import Client, TestCase
from parameterized import parameterized

from api.models import Exam, ExamRegistration, Room, Subject, User


users = [
    (1, "student.1@edu.hse.ru", "1234"),
    (2, "student.2@edu.hse.ru", "9876"),
    (3, "student.3@edu.hse.ru", "password"),
]


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
        User.objects.create(email="student.1@edu.hse.ru", password="12345678")
        subject = Subject.objects.create(subject_name="math")
        room = Room.objects.create(room_number=101)
        room2 = Room.objects.create(room_number=102)
        room3 = Room.objects.create(room_number=103)
        room4 = Room.objects.create(room_number=104)
        Exam.objects.create(subject_id=subject, room_id=room)
        Exam.objects.create(subject_id=subject, room_id=room2)
        Exam.objects.create(subject_id=subject, room_id=room3)
        Exam.objects.create(subject_id=subject, room_id=room4)

    def test_email_is_not_valid(self):
        data = {
            "user_email": "student.edu.hse.ru",
            "exams": [
                {"subject_name": "math", "room_number": 101},
            ],
        }
        response = Client().post(
            "/api/register_for_exams/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"status": "error", "description": "Request data isn't valid"},
        )

    def test_exams_is_not_valid(self):
        data = {
            "user_email": "student@edu.hse.ru",
            "exams": [],
        }
        response = Client().post(
            "/api/register_for_exams/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"status": "error", "description": "Request data isn't valid"},
        )

    def test_one_registration_work(self):
        data = {
            "user_email": "student.1@edu.hse.ru",
            "exams": [{"subject_name": "math", "room_number": 101}],
        }
        response = Client().post(
            "/api/register_for_exams/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "description": "User successfully registered to exams",
            },
        )
        self.assertEqual(ExamRegistration.objects.all().count(), 1)

    def test_many_registration_work(self):
        data = {
            "user_email": "student.1@edu.hse.ru",
            "exams": [
                {"subject_name": "math", "room_number": 101},
                {"subject_name": "math", "room_number": 102},
                {"subject_name": "math", "room_number": 103},
                {"subject_name": "math", "room_number": 104},
            ],
        }
        response = Client().post(
            "/api/register_for_exams/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "description": "User successfully registered to exams",
            },
        )
        self.assertEqual(ExamRegistration.objects.all().count(), 4)
