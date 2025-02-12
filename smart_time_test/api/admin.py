from django.contrib import admin

from api.models import Exam, ExamRegistration, Room, Subject, User

admin.site.register(Room)
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(ExamRegistration)
