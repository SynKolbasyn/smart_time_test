from hashlib import sha3_512
from http import HTTPStatus
from json import dumps

from django.test import Client, TestCase

from api.models import Exam, ExamRegistration, Room, Subject, User


class ExamUnregistrationsTests(TestCase):
    def setUp(self):
        email = "student@edu.hse.ru"
        password = sha3_512(b"12345678").hexdigest()
        user = User.objects.create(email=email, password=password)
        room = Room.objects.create(room_number=1)
        subject = Subject.objects.create(subject_name="math")
        exam = Exam.objects.create(subject_id=subject, room_id=room)
        ExamRegistration.objects.create(user=user, exam=exam)

        Room.objects.create(room_number=10)
        Subject.objects.create(subject_name="rus")

        email = "student.1@edu.hse.ru"
        user = User.objects.create(email=email, password=password)

    def test_bad_email(self):
        data = {
            "email": "student.edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 1,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_wrong_email(self):
        data = {
            "email": "student.2@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 1,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        message = "Email or password invalid"
        expected = {"status": "error", "description": message}
        self.assertDictEqual(response.json(), expected)

    def test_bad_password(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "1234",
            "subject_name": "math",
            "room_number": 1,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_wrong_password(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "123456789",
            "subject_name": "math",
            "room_number": 1,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        message = "Email or password invalid"
        expected = {"status": "error", "description": message}
        self.assertDictEqual(response.json(), expected)

    def test_wrong_subject(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "hist",
            "room_number": 1,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        message = "Subject not found"
        expected = {"status": "error", "description": message}
        self.assertDictEqual(response.json(), expected)

    def test_wrong_room(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 2,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        message = "Room not found"
        expected = {"status": "error", "description": message}
        self.assertDictEqual(response.json(), expected)

    def test_exam_does_not_exists(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "rus",
            "room_number": 10,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        message = "Exam not found with "
        f"subject {data['subject_name']} and room {data['room_number']}"
        expected = {"status": "error", "description": message}
        self.assertDictEqual(response.json(), expected)

    def test_user_not_registered_for_exam(self):
        data = {
            "email": "student.1@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 1,
        }
        response = Client().delete(
            "/api/unregister_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        message = "User not registered for exam with "
        f"subject {data['subject_name']} and room {data['room_number']}"
        expected = {"status": "error", "description": message}
        self.assertDictEqual(response.json(), expected)

    def test_unregister_success(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 1,
        }
        response = Client().delete(
            "/api/unregister_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
