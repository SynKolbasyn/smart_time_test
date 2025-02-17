from django.contrib.admin import site

from exam_organization.models import (
    Campus, Exam, Group, Room, Student, Subject, SubjectUnit, Teacher
)


site.register(Campus)
site.register(Exam)
site.register(Subject)
site.register(SubjectUnit)
site.register(Teacher)
site.register(Group)
site.register(Student)
site.register(Room)
