from django.db.models import (
    CASCADE,
    EmailField,
    ForeignKey,
    IntegerField,
    Model,
    TextField,
)


class Room(Model):
    room_number = IntegerField()

    class Meta:
        db_table = "rooms"


class User(Model):
    email = EmailField(unique=True, blank=False, null=False)
    password = TextField(blank=False, null=False)

    class Meta:
        db_table = "users"


class Subject(Model):
    subject_name = TextField()

    class Meta:
        db_table = "subjects"


class Exam(Model):
    subject_id = ForeignKey(Subject, on_delete=CASCADE)
    room_id = ForeignKey(Room, on_delete=CASCADE)

    class Meta:
        db_table = "exams"


class ExamRegistration(Model):
    exam = ForeignKey(Exam, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        db_table = "exam_registrations"
