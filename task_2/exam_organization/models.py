from django.db.models import (
    CASCADE, CharField, ForeignKey, IntegerField, Model, TextChoices, TextField
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
    patronymic = TextField(unique=False, blank=False, null=False)

    passport_number = IntegerField(unique=True, blank=False, null=False)

    type = TextField(
        choices=TeacherType, unique=False, blank=False, null=False
    )

    class Meta:
        db_table = "teachers"


class Exam(Model):
    subject_unit = ForeignKey(SubjectUnit, CASCADE)

    class Meta:
        db_table = "exams"
