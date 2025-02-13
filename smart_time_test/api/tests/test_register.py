from hashlib import sha3_512
from http import HTTPStatus
from json import dumps

from django.test import Client, TestCase

from api.models import User


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
