from hashlib import sha3_512
from http import HTTPStatus

from django.test import Client, TestCase
from parameterized import parameterized

from api.models import Exam, ExamRegistration, Room, Subject, User


class UserExamRegistrationsTests(TestCase):
    def setUp(self):
        password = sha3_512(b"12345678").hexdigest()
        email = "student.1@edu.hse.ru"
        user1 = User.objects.create(email=email, password=password)
        email = "student.2@edu.hse.ru"
        user2 = User.objects.create(email=email, password=password)
        email = "student.3@edu.hse.ru"
        user3 = User.objects.create(email=email, password=password)
        email = "student.4@edu.hse.ru"
        User.objects.create(email=email, password=password)

        room1 = Room.objects.create(room_number=1)
        room2 = Room.objects.create(room_number=1)
        room3 = Room.objects.create(room_number=1)
        room4 = Room.objects.create(room_number=1)
        room5 = Room.objects.create(room_number=1)

        subject1 = Subject.objects.create(subject_name="math")
        subject2 = Subject.objects.create(subject_name="hist")
        subject3 = Subject.objects.create(subject_name="russ")

        exam1 = Exam.objects.create(subject_id=subject1, room_id=room1)
        exam2 = Exam.objects.create(subject_id=subject1, room_id=room2)
        exam3 = Exam.objects.create(subject_id=subject2, room_id=room3)
        exam4 = Exam.objects.create(subject_id=subject2, room_id=room4)
        exam5 = Exam.objects.create(subject_id=subject3, room_id=room5)

        ExamRegistration.objects.create(user=user1, exam=exam1)
        ExamRegistration.objects.create(user=user1, exam=exam3)
        ExamRegistration.objects.create(user=user1, exam=exam5)
        ExamRegistration.objects.create(user=user2, exam=exam2)
        ExamRegistration.objects.create(user=user2, exam=exam4)
        ExamRegistration.objects.create(user=user2, exam=exam5)
        ExamRegistration.objects.create(user=user3, exam=exam2)
        ExamRegistration.objects.create(user=user3, exam=exam5)

    def test_user_not_found(self):
        response = Client().get("/api/users/5/")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        message = "User not found"
        expected = {"status": "error", "description": message}
        self.assertDictEqual(response.json(), expected)

    @parameterized.expand(
        [
            (1, [1, 3, 5]),
            (2, [2, 4, 5]),
            (3, [2, 5]),
            (4, []),
        ]
    )
    def test_users(self, user_id, exams_id):
        response = Client().get(f"/api/users/{user_id}/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected = {
            "email": f"student.{user_id}@edu.hse.ru",
            "exams": exams_id,
        }
        self.assertDictEqual(response.json(), expected)
