from django.db.models import (
    CASCADE,
    EmailField,
    ForeignKey,
    IntegerField,
    Model,
    TextField,
)


class Room(Model):
    rum_number = IntegerField()

    class Meta:
        db_table = "rooms"


class User(Model):
    email = EmailField()
    password = TextField()

    class Meta:
        db_table = "users"


class Exam(Model):
    subject_name = TextField()
    room_id = ForeignKey(Room, on_delete=CASCADE)

    class Meta:
        db_table = "exams"
