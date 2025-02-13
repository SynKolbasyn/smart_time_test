from http import HTTPStatus
from json import dumps

from django.test import Client, TestCase

from api.models import Exam, Room, Subject


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
