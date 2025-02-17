from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    SET_NULL,
    TextChoices,
    TextField,
)


class Subject(Model):
    name = TextField(unique=True, blank=False, null=False)
    abbreviation = TextField(unique=True, blank=False, null=False)
    unique_id = IntegerField(unique=True, blank=False, null=False)

    class Meta:
        db_table = "subjects"


class Campus(Model):
    name = TextField(unique=True, blank=False, null=False)
    abbreviation = CharField(
        max_length=1, unique=True, blank=False, null=False
    )

    class Meta:
        db_table = "campuses"


class SubjectUnit(Model):
    class GroupType(TextChoices):
        FLOW = "П"
        GROUP = "Г"
        SUB_GROUP = "С"

    campus = ForeignKey(Campus, CASCADE)
    subject = ForeignKey(Subject, CASCADE)
    group_type = CharField(
        max_length=1, choices=GroupType, unique=False, blank=False, null=False
    )
    group_number = IntegerField(unique=True, blank=False, null=False)

    class Meta:
        db_table = "subject_units"


class Teacher(Model):
    class TeacherType(TextChoices):
        LECTURER = "lecturer"
        SEMINARIAN = "seminarian"

    forename = TextField(unique=False, blank=False, null=False)
    surname = TextField(unique=False, blank=False, null=False)
    patronymic = TextField(unique=False, blank=False, null=True)

    passport_number = IntegerField(unique=True, blank=False, null=False)

    type = TextField(
        choices=TeacherType, unique=False, blank=False, null=False
    )
    related_exam = ForeignKey("Exam", SET_NULL, unique=False, null=True)

    class Meta:
        db_table = "teachers"


class Group(Model):
    name = TextField(unique=True, blank=False, null=False)

    class Meta:
        db_table = "groups"


class Student(Model):
    forename = TextField(unique=False, blank=False, null=False)
    surname = TextField(unique=False, blank=False, null=False)
    patronymic = TextField(unique=False, blank=False, null=True)

    passport_number = IntegerField(unique=True, blank=False, null=False)

    group = ForeignKey(Group, CASCADE)

    class Meta:
        db_table = "students"


class Room(Model):
    class RoomType(TextChoices):
        LECTURE_HALL = "лекторий"
        LABORATORY = "лаборатория"
        COMMON = "обычный"
        ONLINE = "онлайн"

    number = IntegerField(unique=True, blank=False, null=True)
    type = TextField(choices=RoomType, unique=False, blank=False, null=False)
    number_of_seats = IntegerField(unique=False, blank=False, null=True)


class Exam(Model):
    class ExamFormat(TextChoices):
        WRITTEN = "письменный"
        ORAL = "устный"

    subject_unit = ForeignKey(SubjectUnit, CASCADE)
    responsible_teacher = ForeignKey(Teacher, CASCADE)
    room = ForeignKey(Room, CASCADE, null=False)

    format = TextField(
        choices=ExamFormat, unique=False, blank=False, null=False
    )
    date_time = DateTimeField(unique=False, blank=False, null=False)

    class Meta:
        db_table = "exams"
