from http import HTTPStatus

from django.test import Client, TestCase
from parameterized import parameterized

from api.models import User


users = [
    (1, "student.1@edu.hse.ru", "1234"),
    (2, "student.2@edu.hse.ru", "9876"),
    (3, "student.3@edu.hse.ru", "password"),
]


class UserTests(TestCase):
    def setUp(self):
        for _, email, password in users:
            User.objects.create(email=email, password=password)

    @parameterized.expand(users)
    def test_user_in_database(self, id, email, password):
        response = Client().get(f"/api/users/{id}/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected = {"id": id, "email": email, "password": password}
        self.assertDictEqual(response.json(), expected)

    def test_user_not_in_database(self):
        response = Client().get("/api/users/4/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        expected = {"description": "User not found"}
        self.assertDictEqual(response.json(), expected)
