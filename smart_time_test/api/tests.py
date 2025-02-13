from hashlib import sha3_512
from http import HTTPStatus
from json import dumps

from django.test import Client, TestCase

from api.models import Exam, ExamRegistration, Room, Subject, User


class RegisterTests(TestCase):
    def setUp(self):
        email = "student@edu.hse.ru"
        password = "12345678"
        User.objects.create(
            email=email, password=sha3_512(password.encode()).hexdigest()
        )

    def test_bad_password(self):
        data = {"email": "student@edu.hse.ru", "password": "1234"}
        response = Client().post(
            "/api/register/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_bad_email(self):
        data = {"email": "student.edu.hse.ru", "password": "12345678"}
        response = Client().post(
            "/api/register/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_user_exists(self):
        data = {"email": "student@edu.hse.ru", "password": "12345678"}
        response = Client().post(
            "/api/register/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_registration_success(self):
        data = {"email": "student.1@edu.hse.ru", "password": "12345678"}
        response = Client().post(
            "/api/register/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ExamRegistrationsTests(TestCase):
    def setUp(self):
        email = "student@edu.hse.ru"
        password = "12345678"
        user = User.objects.create(
            email=email, password=sha3_512(password.encode()).hexdigest()
        )
        room = Room.objects.create(room_number=1)
        subject = Subject.objects.create(subject_name="math")
        exam = Exam.objects.create(subject_id=subject, room_id=room)
        ExamRegistration.objects.create(user=user, exam=exam)

        Room.objects.create(room_number=10)
        Subject.objects.create(subject_name="rus")

        email = "student.1@edu.hse.ru"
        User.objects.create(
            email=email, password=sha3_512(password.encode()).hexdigest()
        )

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

    def test_user_already_registered_for_exam(self):
        data = {
            "email": "student@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 1,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        message = "User already registered for exam with "
        f"subject {data['subject_name']} and room {data['room_number']}"
        expected = {"status": "error", "description": message}
        self.assertDictEqual(response.json(), expected)

    def test_exam_registration_success(self):
        data = {
            "email": "student.1@edu.hse.ru",
            "password": "12345678",
            "subject_name": "math",
            "room_number": 1,
        }
        response = Client().post(
            "/api/register_for_exam/", dumps(data), "application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected = {
            "status": "ok",
            "description": "User successfully registered for exam",
        }
        self.assertDictEqual(response.json(), expected)


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
