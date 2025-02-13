from django.db.models import (
    CASCADE,
    EmailField,
    ForeignKey,
    IntegerField,
    Model,
    OneToOneField,
    TextField,
)


class Room(Model):
    room_number = IntegerField(unique=False, blank=False, null=False)

    class Meta:
        db_table = "rooms"


class User(Model):
    email = EmailField(unique=True, blank=False, null=False)
    password = TextField(blank=False, null=False)

    class Meta:
        db_table = "users"


class Subject(Model):
    subject_name = TextField(unique=False, blank=False, null=False)

    class Meta:
        db_table = "subjects"


class Exam(Model):
    subject_id = ForeignKey(
        Subject, on_delete=CASCADE, unique=False, blank=False, null=False
    )
    room_id = OneToOneField(
        Room, on_delete=CASCADE, unique=True, blank=False, null=False
    )

    class Meta:
        db_table = "exams"


class ExamRegistration(Model):
    exam = ForeignKey(
        Exam, on_delete=CASCADE, unique=False, blank=False, null=False
    )
    user = ForeignKey(
        User, on_delete=CASCADE, unique=False, blank=False, null=False
    )

    class Meta:
        db_table = "exam_registrations"
        unique_together = ("exam", "user")
