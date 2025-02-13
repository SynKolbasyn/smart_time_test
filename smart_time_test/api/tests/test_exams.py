from http import HTTPStatus

from django.test import Client, TestCase

from api.models import Exam, Room, Subject


class ExamsTests(TestCase):
    room_numbers = list(range(1, 6))
    subject_names = ["math", "physics", "chemistry", "biology", "rus"]

    def setUp(self):
        rooms = []
        for room_number in ExamsTests.room_numbers:
            rooms.append(Room.objects.create(room_number=room_number))

        subjects = []
        for subject_name in ExamsTests.subject_names:
            subjects.append(Subject.objects.create(subject_name=subject_name))

        for room, subject in zip(rooms, subjects):
            Exam.objects.create(room_id=room, subject_id=subject)

    def test_get_exams(self):
        response = Client().get("/api/exams/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected = []
        data = zip(
            range(1, 6),
            ExamsTests.room_numbers,
            ExamsTests.subject_names
        )
        for id, room_number, subject_name in data:
            expected.append(
                {
                    "id": id,
                    "room_number": room_number,
                    "subject_name": subject_name,
                }
            )
        self.assertListEqual(response.json(), expected)
